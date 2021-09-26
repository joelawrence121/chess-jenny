import mysql.connector


class ChessDb:
    SINGLE_MOVE_INSERT_QUERY = "INSERT INTO Single_Move (starting_fen, ending_fen, move, gain, type, to_move) VALUES (%s, %s, %s, %s, %s, %s)"
    MATE_IN_N_INSERT_QUERY = "INSERT INTO Mate_In_N (starting_fen, ending_fen, move_list, to_move, moves_to_mate) VALUES (%s, %s, %s, %s, %s)"

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="", database="chess_db"
        )

    def insert_single_move_puzzle(self, starting_fen, ending_fen, move, gain, puzzle_type, to_move):
        values = (starting_fen, ending_fen, move, gain, puzzle_type, to_move)
        cursor = self.db.cursor()
        cursor.execute(self.SINGLE_MOVE_INSERT_QUERY, values)
        self.db.commit()

    def insert_mate_in_N_puzzle(self, starting_fen, ending_fen, moves_to_mate, to_move):
        if len(moves_to_mate) > 1:
            values = (starting_fen, ending_fen, str(moves_to_mate), to_move, len(moves_to_mate))
            cursor = self.db.cursor()
            cursor.execute(self.MATE_IN_N_INSERT_QUERY, values)
            self.db.commit()
