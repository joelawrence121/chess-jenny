from domain.domain import EngineSkillLevel
from generator import generator

if __name__ == '__main__':

    # could randomise the skill levels to add some spice
    generator = generator(EngineSkillLevel.TWO.value, EngineSkillLevel.TEN.value)

    while True:
        try:
            generator.generate_gain()
            generator.reset()
            generator.generate_swing()
            generator.reset()
        except Exception:
            generator.reset()
