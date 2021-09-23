class GAIN_THRESHOLDS:
    ADVANTAGE_GAIN = 400
    SWING_MIN = -50
    SWING_MAX = 100
    CP_GAP = 600

    @staticmethod
    def is_advantage_gain(prev_score, current_score):
        if prev_score is None or current_score is None:
            return False
        elif current_score - prev_score > GAIN_THRESHOLDS.ADVANTAGE_GAIN:
            print("ADVANTAGE GAIN")
            return True

        return False

    @staticmethod
    def is_advantage_swing(prev_score, current_score):
        if prev_score is None or current_score is None:
            return False
        elif prev_score < GAIN_THRESHOLDS.SWING_MIN and current_score > GAIN_THRESHOLDS.SWING_MAX:
            print("ADVANTAGE SWING " + str(prev_score) + " " + str(current_score))
            return True

        return False


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

