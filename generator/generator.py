import math

import chess
import chess.svg
import chess.engine
import mysql.connector

from domain.domain import ENGINE_SKILL_LEVEL, GAIN_THRESHOLDS
from stockfish.stockfish import Engine


class generator:

    def __init__(self, level_1, level_2):
        self.w_engine_level = level_1
        self.w_engine = Engine(level_1)
        self.b_engine_level = level_2
        self.b_engine = Engine(level_2)
        self.board = chess.Board()

    def play_move(self, engine, pov):
        result = engine.play(self.board)
        self.board.push(result.move)
        info = engine.engine.analyse(self.board, chess.engine.Limit(time=0.500))
        cp = chess.engine.PovScore(info['score'], pov).pov(pov).relative.score()
        raw_score = 2 / (1 + math.exp(-0.004 * cp)) - 1

        print(result)
        print(self.board.board_fen())
        print(raw_score)

        return raw_score

    def generate_gain(self):
        w_prev_score = b_prev_score = 0

        while not self.board.is_game_over():
            # whites move
            w_current_score = self.play_move(self.w_engine, chess.WHITE)
            GAIN_THRESHOLDS.is_advantage_gain(w_prev_score, w_current_score)
            w_prev_score = w_current_score

            # blacks move
            b_current_score = self.play_move(self.b_engine, chess.BLACK)
            GAIN_THRESHOLDS.is_advantage_gain(b_prev_score, b_current_score)
            b_prev_score = b_current_score

        print("Checkmate: " + str(self.board.is_checkmate()))
        self.w_engine.engine.quit()
        self.b_engine.engine.quit()

    def generate_swing(self):
        w_prev_score = b_prev_score = 0

        while not self.board.is_game_over():
            # whites move
            w_current_score = self.play_move(self.w_engine, chess.WHITE)
            GAIN_THRESHOLDS.is_advantage_swing(w_prev_score, w_current_score)
            w_prev_score = w_current_score

            # blacks move
            b_current_score = self.play_move(self.b_engine, chess.BLACK)
            GAIN_THRESHOLDS.is_advantage_swing(b_prev_score, b_current_score)
            b_prev_score = b_current_score

            # if gap is too large, swap skill sets
            if b_current_score - w_current_score > GAIN_THRESHOLDS.CP_GAP:
                print("Swapped levels")
                self.w_engine.reconfigure(self.b_engine_level)
                self.b_engine.reconfigure(self.w_engine_level)

        print("Checkmate: " + str(self.board.is_checkmate()))
        self.w_engine.engine.quit()
        self.b_engine.engine.quit()


if __name__ == '__main__':
    generator = generator(ENGINE_SKILL_LEVEL.TWO, ENGINE_SKILL_LEVEL.SIX)
    generator.generate_swing()
