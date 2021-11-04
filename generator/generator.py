import math
import uuid

import chess
import chess.engine
import chess.svg

from data.domain import GainThresholds, EngineSkillLevel
from data.persistence import ChessDb
from stockfish.stockfish import Engine


def normalise(score):
    return score * -1


class Generator(object):
    TIME_LIMIT = 0.1
    MATE_IN_N_LIMIT = 5
    WHITE = "WHITE"
    BLACK = "BLACK"
    GAIN = "GAIN"
    SWING = "SWING"
    MATE = "MATE"
    PIN = "PIN"

    def __init__(self, w_level, b_level):
        self.w_engine_level = w_level
        self.w_engine = Engine(w_level)
        self.b_engine_level = b_level
        self.b_engine = Engine(b_level)
        self.board = chess.Board()
        self.db = ChessDb()

    def reset(self):
        self.w_engine = Engine(self.w_engine_level)
        self.b_engine = Engine(self.b_engine_level)
        self.board = chess.Board()

    def other_turn(self, turn):
        if turn == self.WHITE:
            return self.BLACK
        return self.WHITE

    def play_move(self, engine, pov):
        result = engine.play(self.board)
        self.board.push(result.move)

        info = engine.engine.analyse(self.board, chess.engine.Limit(time=self.TIME_LIMIT))
        pov_score = chess.engine.PovScore(info['score'], pov).pov(pov)
        cp = pov_score.relative.score()

        raw_score = None
        if not pov_score.is_mate():
            raw_score = normalise(2 / (1 + math.exp(-0.004 * cp)) - 1)

        # print(("white" if pov else "black") + " played " + result.move.uci() + ": \t" + str(raw_score))
        return raw_score, result.move, pov_score

    def check_and_persist_puzzles(self, game_id, move, pov_score, previous_fen, current_score, prev_score, turn):
        # advantage gain check
        if GainThresholds.is_advantage_gain(prev_score, current_score):
            self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move.uci(), current_score - prev_score,
                                              self.GAIN, turn, None)

        # advantage swing check
        if GainThresholds.is_advantage_swing(prev_score, current_score):
            self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move.uci(), current_score - prev_score,
                                              self.SWING, turn, None)

        # mate in 1 check
        if self.board.is_checkmate():
            self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move.uci(), None, self.MATE, turn, None)

        # mate in N check
        if pov_score.is_mate() and normalise(pov_score.relative.mate()) in range(0, self.MATE_IN_N_LIMIT):
            mate_in_N = normalise(pov_score.relative.mate())
            self.db.insert_mate_in_N_puzzle(self.board.fen(), self.other_turn(turn), mate_in_N, game_id)

        # king pin check (only persist when playing optimally)
        if self.board.is_pinned(turn == self.WHITE, move.to_square) \
                and self.w_engine_level == EngineSkillLevel.TEN.value \
                and self.b_engine_level == EngineSkillLevel.TEN.value:
            board_copy = self.board.copy()
            follow_move = board_copy.pop()
            pin_move = board_copy.pop()
            self.db.insert_single_move_puzzle(board_copy.fen(), self.board.fen(), pin_move.uci(), None, self.PIN,
                                              self.other_turn(turn), follow_move.uci())

    def switch_engine_levels(self, b_current_score, w_current_score):
        if b_current_score is None or w_current_score is None:
            return
        if b_current_score - w_current_score > GainThresholds.CP_GAP.value:
            self.w_engine.reconfigure(self.b_engine_level)
            self.b_engine.reconfigure(self.w_engine_level)

    def play_game(self, allow_skill_switch):
        print(str() + "Starting game: " + uuid.uuid4().hex)
        game_id = self.db.insert_game(self)

        w_prev_score = b_prev_score = 0
        while not self.board.is_game_over():

            # whites move
            previous_fen = self.board.fen()
            w_move_result = self.play_move(self.w_engine, chess.WHITE)
            w_current_score = w_move_result[0]
            move = w_move_result[1]
            pov_score = w_move_result[2]
            self.check_and_persist_puzzles(game_id, move, pov_score, previous_fen, w_current_score, w_prev_score,
                                           self.WHITE)
            w_prev_score = w_current_score
            if self.board.is_game_over(): break

            # blacks move
            previous_fen = self.board.fen()
            b_move_result = self.play_move(self.b_engine, chess.BLACK)
            b_current_score = b_move_result[0]
            move = b_move_result[1]
            pov_score = b_move_result[2]
            self.check_and_persist_puzzles(game_id, move, pov_score, previous_fen, b_current_score, b_prev_score,
                                           self.BLACK)
            b_prev_score = b_current_score
            if self.board.is_game_over(): break

            # switch engine levels if scores are too far apart
            if allow_skill_switch:
                self.switch_engine_levels(b_current_score, w_current_score)

        self.db.update_game(game_id, self.board.result())
        self.w_engine.engine.quit()
        self.b_engine.engine.quit()
