import math

import chess
import chess.engine
import chess.svg

from domain.domain import EngineSkillLevel, GainThresholds
from stockfish.stockfish import Engine


class generator:

    def __init__(self, w_level, b_level):
        self.w_engine_level = w_level
        self.w_engine = Engine(w_level)
        self.b_engine_level = b_level
        self.b_engine = Engine(b_level)
        self.board = chess.Board()

    def play_move(self, engine, pov):
        result = engine.play(self.board)
        self.board.push(result.move)
        info = engine.engine.analyse(self.board, chess.engine.Limit(time=0.500))

        if pov is True:
            cp = chess.engine.PovScore(info['score'], pov).white().relative.score()
        else:
            cp = chess.engine.PovScore(info['score'], pov).black().relative.score()

        raw_score = None
        if cp is not None:
            raw_score = (2 / (1 + math.exp(-0.004 * cp)) - 1) * -1

        print(result)
        print(self.board.board_fen())
        print(str(pov) + str(raw_score))

        return raw_score

    def generate_gain(self):
        w_prev_score = b_prev_score = 0

        while not self.board.is_game_over():
            # whites move
            w_current_score = self.play_move(self.w_engine, chess.WHITE)
            GainThresholds.is_advantage_gain(w_prev_score, w_current_score)
            w_prev_score = w_current_score

            # blacks move
            b_current_score = self.play_move(self.b_engine, chess.BLACK)
            GainThresholds.is_advantage_gain(b_prev_score, b_current_score)
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
            w_current_score = self.play_move(self.w_engine, chess.WHITE)
            GainThresholds.is_advantage_swing(w_prev_score, w_current_score)
            print("WHITE " + str(w_prev_score) + " -> " + str(w_current_score))
            w_prev_score = w_current_score

            # blacks move
            b_current_score = self.play_move(self.b_engine, chess.BLACK)
            GainThresholds.is_advantage_swing(b_prev_score, b_current_score)
            print("BLACK " + str(b_prev_score) + " -> " + str(b_current_score))
            b_prev_score = b_current_score

            # if gap is too large, swap skill sets
            self.reconfigure_engine_levels(b_current_score, w_current_score)

        print("Checkmate: " + str(self.board.is_checkmate()))
        print()
        self.w_engine.engine.quit()
        self.b_engine.engine.quit()


if __name__ == '__main__':
    generator = generator(EngineSkillLevel.TWO.value, EngineSkillLevel.TEN.value)
    generator.generate_gain()
