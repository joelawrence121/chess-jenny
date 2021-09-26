import random

from domain.domain import EngineSkillLevel
from generator import generator

import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    while True:
        engine_levels = list(EngineSkillLevel)
        # jenny = generator(random.choice(engine_levels).value, random.choice(engine_levels).value)
        jenny = generator(1, 10)
        try:
            jenny.play_game(False)
            jenny.reset()
            jenny.play_game(True)
            jenny.reset()
        except Exception as e:
            logging.warning("An exception was thrown: " + str(e))
            jenny.reset()
