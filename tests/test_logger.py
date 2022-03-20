import unittest

from .context import GameLog, GameLogLevel, GameScore, Timer, status as s
from .fixture import MockBuffer

class TestGameLog(unittest.TestCase):

    def test_log_debug_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="DEBUG")
        
        logger.log_debug("debug")

        self.assertEqual(buffer.content, "DEBUG : debug\n")

    def test_log_debug_when_level_not_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.INFO)
        
        logger.log_debug("debug")

        self.assertEqual(buffer.content, "")

    def test_log_info_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="INFO")
        
        logger.log_info("info")

        self.assertEqual(buffer.content, "INFO  : info\n")

    def test_log_info_when_level_not_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.ACTION)
        
        logger.log_info("info")

        self.assertEqual(buffer.content, "")


    def test_log_game_status_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="ACTION")

        logger.log_game_status(s.GameStatus.FIRST_QUARTER)

        self.assertEqual(buffer.content, "STATUS: First Quarter\n")


    def test_log_game_status_when_level_not_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.SCORE)

        logger.log_game_status(s.GameStatus.FIRST_QUARTER)

        self.assertEqual(buffer.content, "")


    def test_log_action_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="ACTION")
        timer = Timer()
        
        logger.log_action(timer, "GOAL!")

        self.assertEqual(buffer.content, "00:00 - GOAL!\n")


    def test_log_action_when_level_not_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.SCORE)
        timer = Timer()

        logger.log_action(timer, "GOAL!")

        self.assertEqual(buffer.content, "")


    def test_log_action_when_lower_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="INFO")
        timer = Timer()
        
        logger.log_action(timer, "GOAL!")

        self.assertEqual(buffer.content, "00:00 - GOAL!\n")


    def test_log_goal_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="SCORE")
        timer = Timer()
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_goal("AAA")
        logger.log_goal(timer, "AAA", score)

        expected = "00:00: GOAL!!: AAA\nAAA 6, BBB 0\n"
        self.assertEqual(buffer.content, expected)


    def test_log_goal_when_level_not_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.QUARTER)
        timer = Timer()
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_goal("AAA")
        logger.log_goal(timer, "AAA", score)

        self.assertEqual(buffer.content, "")


    def test_log_goal_when_lower_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="ACTION")
        timer = Timer()
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_goal("AAA")
        logger.log_goal(timer, "AAA", score)

        expected = "00:00: GOAL!!: AAA\nAAA 6, BBB 0\n"
        self.assertEqual(buffer.content, expected)


    def test_log_behind_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="SCORE")
        timer = Timer()
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_behind("AAA")
        logger.log_behind(timer, "AAA", score)

        expected = "00:00: BEHIND: AAA\nAAA 1, BBB 0\n"
        self.assertEqual(buffer.content, expected)


    def test_log_behind_when_level_not_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.QUARTER)
        timer = Timer()
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_behind("AAA")
        logger.log_behind(timer, "AAA", score)

        self.assertEqual(buffer.content, "") 


    def test_log_behind_when_lower_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="ACTION")
        timer = Timer()
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_behind("AAA")
        logger.log_behind(timer, "AAA", score)

        expected = "00:00: BEHIND: AAA\nAAA 1, BBB 0\n"
        self.assertEqual(buffer.content, expected)


    def test_log_quarter_time_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.QUARTER)
        score = GameScore("AAA", "BBB")

        score.set_status(s.GameStatus.FIRST_QUARTER)
        score.score_behind("AAA")
        score.score_goal("BBB")
        score.set_status(s.GameStatus.SECOND_QUARTER)
        logger.log_quarter_time(s.GameStatus.QUARTER_TIME, score)

        expected = "** 1/4 Time **\nAAA: 0. 1. 1\nBBB: 1. 0. 6\n\n"
        self.assertEqual(buffer.content, expected)


    def test_log_quarter_time_when_level_not_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="FINAL")
        score = GameScore("AAA", "BBB")

        score.set_status(s.GameStatus.FIRST_QUARTER)
        score.score_behind("AAA")
        score.score_goal("BBB")
        score.set_status(s.GameStatus.SECOND_QUARTER)
        logger.log_quarter_time(s.GameStatus.QUARTER_TIME, score)

        self.assertEqual(buffer.content, "")


    def test_log_quarter_time_when_lower_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="SCORE")
        score = GameScore("AAA", "BBB")

        score.set_status(s.GameStatus.FIRST_QUARTER)
        score.score_behind("AAA")
        score.score_goal("BBB")
        score.set_status(s.GameStatus.SECOND_QUARTER)
        logger.log_quarter_time(s.GameStatus.QUARTER_TIME, score)

        expected = "** 1/4 Time **\nAAA: 0. 1. 1\nBBB: 1. 0. 6\n\n"
        self.assertEqual(buffer.content, expected)
   

    def test_log_final_result_winner_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.FINAL)
        score = GameScore("AAA", "BBB")

        score.set_status(s.GameStatus.FIRST_QUARTER)
        score.set_status(s.GameStatus.SECOND_QUARTER)
        score.set_status(s.GameStatus.THIRD_QUARTER)
        score.set_status(s.GameStatus.FOURTH_QUARTER)
        score.score_behind("AAA")
        score.score_goal("BBB")
        score.set_status(s.GameStatus.FULL_TIME)

        logger.log_final_result(score)

        expected = "** Full Time **\nAAA: 0. 1. 1\nBBB: 1. 0. 6\n\n"
        expected += "RESULT: BBB WON by 5 points\n"
        self.assertEqual(buffer.content, expected)


    def test_log_final_result_draw_when_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level=GameLogLevel.FINAL)
        score = GameScore("AAA", "BBB")

        score.set_status(s.GameStatus.FIRST_QUARTER)
        score.set_status(s.GameStatus.SECOND_QUARTER)
        score.set_status(s.GameStatus.THIRD_QUARTER)
        score.set_status(s.GameStatus.FOURTH_QUARTER)
        score.score_goal("AAA")
        score.score_goal("BBB")
        score.set_status(s.GameStatus.FULL_TIME)

        logger.log_final_result(score)

        expected = "** Full Time **\nAAA: 1. 0. 6\nBBB: 1. 0. 6\n\n"
        expected += "RESULT: DRAW\n"
        self.assertEqual(buffer.content, expected)


    def test_log_final_result_winner_when_lower_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="SCORE")
        score = GameScore("AAA", "BBB")

        score.set_status(s.GameStatus.FIRST_QUARTER)
        score.set_status(s.GameStatus.SECOND_QUARTER)
        score.set_status(s.GameStatus.THIRD_QUARTER)
        score.set_status(s.GameStatus.FOURTH_QUARTER)
        score.score_behind("AAA")
        score.score_goal("BBB")
        score.set_status(s.GameStatus.FULL_TIME)

        logger.log_final_result(score)

        expected = "RESULT: BBB WON by 5 points\n"
        self.assertEqual(buffer.content, expected)


    def test_log_final_result_draw_when_lower_level_set(self):
        buffer = MockBuffer()
        logger = GameLog(buffer, level="SCORE")
        score = GameScore("AAA", "BBB")

        score.set_status(s.GameStatus.FIRST_QUARTER)
        score.set_status(s.GameStatus.SECOND_QUARTER)
        score.set_status(s.GameStatus.THIRD_QUARTER)
        score.set_status(s.GameStatus.FOURTH_QUARTER)
        score.score_goal("AAA")
        score.score_goal("BBB")
        score.set_status(s.GameStatus.FULL_TIME)

        logger.log_final_result(score)

        expected = "RESULT: DRAW\n"
        self.assertEqual(buffer.content, expected)

