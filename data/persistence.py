import configparser
import logging

import mysql.connector


class ChessDb(object):
    PERSISTENCE_EXCEPTION_MESSAGE = "An exception was thrown during persistence: {}"

    GAME_INSERT_QUERY = "INSERT INTO Game (white_level, black_level) VALUES (%s, %s)"
    GAME_UPDATE_QUERY = "UPDATE Game SET outcome = %s WHERE Id = %s"
    SINGLE_MOVE_INSERT_QUERY = "INSERT INTO Single_Move (starting_fen, ending_fen, move, gain, type, to_move, follow_move) VALUES " \
                               "(%s, %s, %s, %s, %s, %s, %s) "
    MATE_IN_N_INSERT_QUERY = "INSERT INTO Mate_In_N (starting_fen, to_move, moves_to_mate, game_id) VALUES (%s, %s, " \
                             "%s, %s) "

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        credentials = config['DB_CREDENTIALS']
        self.db = mysql.connector.connect(
            host=credentials['host'],
            user=credentials['user'],
            password=credentials['password'],
            database='chess_db'
        )

    def insert_single_move_puzzle(self, starting_fen, ending_fen, move, gain, puzzle_type, to_move, follow_move):
        values = (starting_fen, ending_fen, move, gain, puzzle_type, to_move, follow_move)
        cursor = self.db.cursor()
        try:
            cursor.execute(self.SINGLE_MOVE_INSERT_QUERY, values)
            self.db.commit()
            print("Inserted: \t single move puzzle \t " + puzzle_type + " \t id: " + str(cursor.lastrowid))
        except Exception as e:
            logging.warning(self.PERSISTENCE_EXCEPTION_MESSAGE.format(str(e)))
        finally:
            cursor.close()

    def insert_mate_in_N_puzzle(self, starting_fen, to_move, moves_to_mate, game_id):
        values = (starting_fen, to_move, moves_to_mate, game_id)
        cursor = self.db.cursor()
        try:
            cursor.execute(self.MATE_IN_N_INSERT_QUERY, values)
            self.db.commit()
            print("Inserted: \t mate in " + str(moves_to_mate) + " \t\t\t id: " + str(cursor.lastrowid))
        except Exception as e:
            logging.warning(self.PERSISTENCE_EXCEPTION_MESSAGE.format(str(e)))
        finally:
            cursor.close()

    def insert_game(self, generator):
        values = (generator.w_engine_level, generator.b_engine_level)
        cursor = self.db.cursor()
        try:
            cursor.execute(self.GAME_INSERT_QUERY, values)
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            logging.warning(self.PERSISTENCE_EXCEPTION_MESSAGE.format(str(e)))
        finally:
            cursor.close()

    def update_game(self, game_id, outcome):
        values = (outcome, game_id)
        cursor = self.db.cursor()
        try:
            cursor.execute(self.GAME_UPDATE_QUERY, values)
            self.db.commit()
        except Exception as e:
            logging.warning(self.PERSISTENCE_EXCEPTION_MESSAGE.format(str(e)))
        finally:
            cursor.close()
