import logging
import random

from data.domain import EngineSkillLevel
from generator import Generator

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    while True:
        engine_levels = list(EngineSkillLevel)
        jenny = Generator(random.choice(engine_levels).value, random.choice(engine_levels).value)
        try:
            jenny.play_game(False)
            jenny.reset()
            jenny.play_game(True)
            jenny.reset()
        except TypeError as e:
            logging.warning("An exception was thrown: " + str(e))
            jenny.reset()
