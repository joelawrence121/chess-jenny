from domain.domain import EngineSkillLevel
from generator import generator

import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    # could randomise the skill levels to add some spice
    generator = generator(EngineSkillLevel.TWO.value, EngineSkillLevel.TEN.value)

    while True:
        try:
            generator.play_game(False)
            generator.reset()
            generator.play_game(True)
            generator.reset()
        except Exception:
            logging.warning("An exception was thrown")
            generator.reset()
