import logging
import random
import threading

from data.domain import EngineSkillLevel
from generator import Generator


def run(t):
    print("Starting thread: " + str(t))
    engine_levels = list(EngineSkillLevel)
    jenny = Generator(random.choice(engine_levels).value, random.choice(engine_levels).value)
    try:
        jenny.play_game(False)
        jenny.reset()
        jenny.play_game(True)
        jenny = Generator(EngineSkillLevel.TEN.value, EngineSkillLevel.TEN.value)
        jenny.play_game(False)
    except TypeError as e:
        logging.warning("An exception was thrown: " + str(e))
        jenny.reset()
    print("Finishing thread: " + str(t))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    threads = list()
    while True:
        for index in range(5):
            thread = threading.Thread(target=run, args=(index,))
            threads.append(thread)
            thread.start()
        for index, thread in enumerate(threads):
            thread.join()
