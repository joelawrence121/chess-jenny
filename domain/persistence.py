import mysql.connector


class ChessDb:
    INSERT_SQL = "INSERT INTO puzzle (starting_fen, ending_fen, move, gain, type, to_move) VALUES (%s, %s, %s, %s, %s, %s)"

    def __init__(self):
        self.db = mydb = mysql.connector.connect(
            host="localhost", user="root", password="", database="chess_db"
        )

    def insert(self, previous_fen, ending_fen, move, gain, puzzle_type, to_move):
        values = (previous_fen, ending_fen, move, gain, puzzle_type, to_move)

        cursor = self.db.cursor()
        cursor.execute(self.INSERT_SQL, values)
        self.db.commit()
