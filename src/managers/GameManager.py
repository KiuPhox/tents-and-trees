from constants.LevelData import LevelData


class GameManager:
    current_level = 1

    @staticmethod
    def next_level():
        GameManager.current_level += 1

    @staticmethod
    def get_current_level_data():
        return LevelData.LEVELS[GameManager.current_level - 1]

    @staticmethod
    def get_level_count() -> int:
        return len(LevelData.LEVELS)
