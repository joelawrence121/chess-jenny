from enum import Enum


class GainThresholds(Enum):
    # -1 definite loss
    # 1 definite win

    ADVANTAGE_GAIN = 0.5
    SWING_MIN = -0.2
    SWING_MAX = 0.1
    CP_GAP = 0.6

    @staticmethod
    def is_advantage_gain(prev_score, current_score):
        if prev_score is None or current_score is None:
            return False
        elif current_score - prev_score > GainThresholds.ADVANTAGE_GAIN.value:
            print("ADVANTAGE GAIN")
            return True

        return False

    @staticmethod
    def is_advantage_swing(prev_score, current_score):
        if prev_score is None or current_score is None:
            return False
        elif prev_score < GainThresholds.SWING_MIN.value and current_score > GainThresholds.SWING_MAX.value:
            print("ADVANTAGE SWING " + str(prev_score) + " " + str(current_score))
            return True

        return False


class EngineSkillLevel(Enum):
    ONE = 1
    TWO = 3
    THREE = 5
    FOUR = 7
    FIVE = 9
    SIX = 11
    SEVEN = 13
    EIGHT = 15
    NINE = 17
    TEN = 19
