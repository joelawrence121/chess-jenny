import math
import uuid

import chess
import chess.engine
import chess.svg

from domain.domain import GainThresholds
from domain.persistence import ChessDb
from stockfish.stockfish import Engine


class generator:
    TIME_LIMIT = 0.1
    MATE_IN_N_LIMIT = 5
    WHITE = "WHITE"
    BLACK = "BLACK"
    GAIN = "GAIN"
    SWING = "SWING"
    MATE = "MATE"

    def __init__(self, w_level, b_level):
        self.w_engine_level = w_level
        self.w_engine = Engine(w_level)
        self.b_engine_level = b_level
        self.b_engine = Engine(b_level)
        self.w_move_stack = []
        self.b_move_stack = []
        self.mate_start_fen = ""
        self.counting_mate = False
        self.board = chess.Board()
        self.db = ChessDb()

    def reset(self):
        self.w_engine = Engine(self.w_engine_level)
        self.b_engine = Engine(self.b_engine_level)
        self.board = chess.Board()

    def play_move(self, engine, pov):
        result = engine.play(self.board)
        self.board.push(result.move)

        info = engine.engine.analyse(self.board, chess.engine.Limit(time=self.TIME_LIMIT))
        pov_score = chess.engine.PovScore(info['score'], pov).pov(pov)
        cp = pov_score.relative.score()

        raw_score = None
        if pov_score.is_mate() is False:
            raw_score = (2 / (1 + math.exp(-0.004 * cp)) - 1) * -1

        print(("white" if pov else "black") + " played " + result.move.uci() + ": \t" + str(raw_score))
        return raw_score, result.move.uci(), pov_score

    def reconfigure_engine_levels(self, b_current_score, w_current_score):
        if b_current_score is None or w_current_score is None:
            return
        if b_current_score - w_current_score > GainThresholds.CP_GAP.value:
            self.w_engine.reconfigure(self.b_engine_level)
            self.b_engine.reconfigure(self.w_engine_level)

    def play_game(self, allow_skill_switch):
        print(str() + "Game: " + uuid.uuid4().hex)

        w_prev_score = b_prev_score = 0
        prev_moves_to_mate = self.MATE_IN_N_LIMIT + 1

        while not self.board.is_game_over():

            # whites move
            previous_fen = self.board.fen()
            w_move_result = self.play_move(self.w_engine, chess.WHITE)
            w_current_score = w_move_result[0]
            move = w_move_result[1]
            pov_score = w_move_result[2]
            print(pov_score)
            if GainThresholds.is_advantage_gain(w_prev_score, w_current_score):
                self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move, w_current_score - w_prev_score,
                                                  self.GAIN, self.WHITE)
            if GainThresholds.is_advantage_swing(w_prev_score, w_current_score):
                self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move, w_current_score - w_prev_score,
                                                  self.SWING, self.WHITE)
            if self.board.is_checkmate():
                self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move, None, self.MATE, self.WHITE)

            w_prev_score = w_current_score

            # blacks move
            previous_fen = self.board.fen()
            b_move_result = self.play_move(self.b_engine, chess.BLACK)
            b_current_score = b_move_result[0]
            move = b_move_result[1]
            pov_score = b_move_result[2]
            print(pov_score)
            if GainThresholds.is_advantage_gain(b_prev_score, b_current_score):
                self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move, b_current_score - b_prev_score,
                                                  self.GAIN, self.BLACK)
            if GainThresholds.is_advantage_swing(b_prev_score, b_current_score):
                self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move, b_current_score - b_prev_score,
                                                  self.SWING, self.BLACK)
            if self.board.is_checkmate():
                self.db.insert_single_move_puzzle(previous_fen, self.board.fen(), move, None, self.MATE, self.BLACK)

            if pov_score.is_mate() and (pov_score.relative.mate() * -1) in range(0, self.MATE_IN_N_LIMIT):

                if self.counting_mate is False:
                    print("Starting fen: " + self.board.fen())
                    self.mate_start_fen = self.board.fen()

                self.counting_mate = True

                current_moves_to_mate = pov_score.relative.mate() * -1
                print("Moves to mate: " + str(current_moves_to_mate))
                if current_moves_to_mate < prev_moves_to_mate:
                    prev_moves_to_mate = current_moves_to_mate
                    self.b_move_stack.append(move)
                    print(self.b_move_stack)

                    if current_moves_to_mate == 0:
                        self.db.insert_mate_in_N_puzzle(self.mate_start_fen, self.board.fen(), self.b_move_stack,
                                                        self.WHITE)
                        self.counting_mate = False
                        self.b_move_stack = []
                        prev_moves_to_mate = self.MATE_IN_N_LIMIT + 1
                        self.mate_start_fen = ""
                else:
                    self.counting_mate = False
                    self.b_move_stack = []
                    prev_moves_to_mate = self.MATE_IN_N_LIMIT + 1
                    self.mate_start_fen = ""

            b_prev_score = b_current_score

            if allow_skill_switch:
                self.reconfigure_engine_levels(b_current_score, w_current_score)

        self.w_engine.engine.quit()
        self.b_engine.engine.quit()
