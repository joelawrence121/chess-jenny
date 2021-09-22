class ENGINE_SKILL_LEVEL:
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10

    @staticmethod
    def get_value(level):
        levels = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        return levels[level - 1]
