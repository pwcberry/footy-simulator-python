import unittest
from logger import GameLog
from status import GameScore, GameStatus, Timer

class MockBuffer:
    content = ""

    def write(self, input):
        self.content = input

class TestGameLog(unittest.TestCase):

    def test_log_short_score(self):
        # Arrange
        buffer = MockBuffer()
        logger = GameLog(buffer)
        score = GameScore("AAA", "BBB")
        timer = Timer()

        # Act
        logger.log_short_score(timer, score)

        # Assert
        self.assertEqual(buffer.content, "00:00 - AAA 0, BBB 0\n")

    def test_log_full_score(self):
        # Arrange
        buffer = MockBuffer()
        logger = GameLog(buffer)
        score = GameScore("AAA", "BBB")

        # Act
        logger.log_full_score(score)

        # Assert
        self.assertEqual(buffer.content, "AAA: 0. 0. 0\nBBB: 0. 0. 0\n")

    def test_log_status(self):
        # Arrange
        buffer = MockBuffer()
        logger = GameLog(buffer)

        # Act
        logger.log_status(GameStatus.QUARTER_TIME)

        # Assert
        self.assertEqual(buffer.content, "Status: QUARTER_TIME\n")

    def test_log_message(self):
        # Arrange
        buffer = MockBuffer()
        logger = GameLog(buffer)
        timer = Timer()

        # Act
        logger.log_message(timer, "GOAL!")

        # Assert
        self.assertEqual(buffer.content, "00:00 - GOAL!\n")


if __name__ == "__main__":
    unittest.main()
