import chess

from domain.domain import ENGINE_SKILL_LEVEL
from stockfish.stockfish import Engine


def generate():
    engine1 = Engine(ENGINE_SKILL_LEVEL.ONE)
    engine2 = Engine(ENGINE_SKILL_LEVEL.SIX)

    board = chess.Board()
    while not board.is_game_over():
        result = engine1.play(board)
        board.push(result.move)
        print("--------------")
        print(result)
        print(board.board_fen())

        result = engine2.play(board)
        board.push(result.move)
        print("--------------")
        print(result)
        print(board.board_fen())

    print("Checkmate: " + board.is_checkmate().__str__())
    engine1.engine.quit()
    engine2.engine.quit()


if __name__ == '__main__':
    generate()