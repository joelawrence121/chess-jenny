import math

import chess
import chess.engine
import chess.svg

from domain.domain import GainThresholds
from domain.persistence import ChessDb
from stockfish.stockfish import Engine


class generator:

    TIME_LIMIT = 0.500

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

    def play_move(self, engine, pov):
        result = engine.play(self.board)
        self.board.push(result.move)
        info = engine.engine.analyse(self.board, chess.engine.Limit(time=self.TIME_LIMIT))
        cp = chess.engine.PovScore(info['score'], pov).pov(pov).relative.score()

        raw_score = None
        if cp is not None:
            raw_score = (2 / (1 + math.exp(-0.004 * cp)) - 1) * -1

        print(result)
        print(self.board.board_fen())
        print(str(pov) + str(raw_score))

        return raw_score, result.move.uci()

    def generate_gain(self):
        w_prev_score = b_prev_score = 0

        while not self.board.is_game_over():
            # whites move
            previous_fen = self.board.fen()
            w_move_result = self.play_move(self.w_engine, chess.WHITE)
            w_current_score = w_move_result[0]
            if GainThresholds.is_advantage_gain(w_prev_score, w_current_score):
                self.db.insert(previous_fen, self.board.fen(), w_move_result[1], w_current_score - w_prev_score, "gain",
                               "white")
            w_prev_score = w_current_score

            # blacks move
            previous_fen = self.board.fen()
            b_move_result = self.play_move(self.b_engine, chess.BLACK)
            b_current_score = b_move_result[0]
            if GainThresholds.is_advantage_gain(b_prev_score, b_current_score):
                self.db.insert(previous_fen, self.board.fen(), b_move_result[1], b_current_score - b_prev_score, "gain",
                               "black")
            b_prev_score = b_current_score

        print("Checkmate: " + str(self.board.is_checkmate()))
        self.w_engine.engine.quit()
        self.b_engine.engine.quit()

    def reconfigure_engine_levels(self, b_current_score, w_current_score):
        if b_current_score is None or w_current_score is None:
            return
        if b_current_score - w_current_score > GainThresholds.CP_GAP.value:
            print("Swapped levels")
            self.w_engine.reconfigure(self.b_engine_level)
            self.b_engine.reconfigure(self.w_engine_level)

    def generate_swing(self):
        w_prev_score = b_prev_score = 0

        while not self.board.is_game_over():
            # whites move
            previous_fen = self.board.fen()
            w_move_result = self.play_move(self.w_engine, chess.WHITE)
            w_current_score = w_move_result[0]
            print("WHITE " + str(w_prev_score) + " -> " + str(w_current_score))

            if GainThresholds.is_advantage_swing(w_prev_score, w_current_score):
                self.db.insert(previous_fen, self.board.fen(), w_move_result[1], w_current_score - w_prev_score,
                               "swing", "white")
            w_prev_score = w_current_score

            # blacks move
            previous_fen = self.board.fen()
            b_move_result = self.play_move(self.b_engine, chess.BLACK)
            b_current_score = b_move_result[0]
            print("BLACK " + str(b_prev_score) + " -> " + str(b_current_score))

            if GainThresholds.is_advantage_swing(b_prev_score, b_current_score):
                self.db.insert(previous_fen, self.board.fen(), b_move_result[1], b_current_score - b_prev_score,
                               "swing", "black")
            b_prev_score = b_current_score

            # if gap is too large, swap skill sets to encourage comeback
            self.reconfigure_engine_levels(b_current_score, w_current_score)

        print("Checkmate: " + str(self.board.is_checkmate()))
        self.w_engine.engine.quit()
        self.b_engine.engine.quit()
