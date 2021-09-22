import chess
import chess.svg
import chess.engine

from domain.domain import ENGINE_SKILL_LEVEL
from stockfish.stockfish import Engine


def print_big_move(prev_score, current_score):
    if prev_score is None or current_score is None:
        return
    if abs(prev_score) - abs(current_score) > 400:
        print("BIG MOVE")


def generate():
    engine1 = Engine(ENGINE_SKILL_LEVEL.TWO)
    engine2 = Engine(ENGINE_SKILL_LEVEL.SIX)

    board = chess.Board()
    w_prev_score = 0
    b_prev_score = 0

    while not board.is_game_over():
        # whites move
        result = engine1.play(board)
        board.push(result.move)
        info = engine1.engine.analyse(board, chess.engine.Limit(depth=10))
        w_current_score = info["score"].pov(True).score()

        print(result)
        print(board.board_fen())
        print("Score:", w_current_score)
        print_big_move(w_prev_score, w_current_score)
        w_prev_score = w_current_score

        # blacks move
        result = engine2.play(board)
        board.push(result.move)
        info = engine2.engine.analyse(board, chess.engine.Limit(depth=10))
        b_current_score = info["score"].pov(False).score()

        print(result)
        print(board.board_fen())
        print("Score:", b_current_score)
        print_big_move(b_prev_score, b_current_score)
        b_prev_score = b_current_score

    print("Checkmate: " + str(board.is_checkmate()))
    engine1.engine.quit()
    engine2.engine.quit()


if __name__ == '__main__':
    generate()
