import unittest

from .context import GameScore, status as s

class TestGameScore(unittest.TestCase):

    def test_score_goal(self):
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_goal("AAA")
        self.assertEqual(score.current_scores["AAA"].goals, 1)

        score.score_goal("BBB")
        self.assertEqual(score.current_scores["BBB"].goals, 1)


    def test_score_behind(self):
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_behind("AAA")
        self.assertEqual(score.current_scores["AAA"].behinds, 1)

        score.score_behind("BBB")
        self.assertEqual(score.current_scores["BBB"].behinds, 1)

    def test_set_status(self):
        score = GameScore("AAA", "BBB")
        
        score.set_status(s.GameStatus.FIRST_QUARTER)
        self.assertEqual(score.quarter, 1)
        self.assertEqual(len(score.quarter_scores["AAA"]), 0)

        score.set_status(s.GameStatus.SECOND_QUARTER)
        self.assertEqual(score.quarter, 2)
        self.assertEqual(len(score.quarter_scores["AAA"]), 1)
        
        score.set_status(s.GameStatus.THIRD_QUARTER)
        self.assertEqual(score.quarter, 3)
        self.assertEqual(len(score.quarter_scores["AAA"]), 2)

        score.set_status(s.GameStatus.FOURTH_QUARTER)
        self.assertEqual(score.quarter, 4)
        self.assertEqual(len(score.quarter_scores["AAA"]), 3)

        score.set_status(s.GameStatus.FULL_TIME)
        self.assertEqual(score.quarter, 5)
        self.assertEqual(len(score.quarter_scores["AAA"]), 4)

    def test_current_scores(self):
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_goal("AAA")
        score.score_goal("BBB")
        score.score_behind("AAA")
        score.score_behind("AAA")
        score.score_goal("BBB")

        self.assertEqual(score.get_current_score(), "AAA: 1. 2. 8\nBBB: 2. 0. 12\n")

    def test_final_score(self):
        score = GameScore("AAA", "BBB")
        score.set_status(s.GameStatus.FIRST_QUARTER)

        score.score_goal("AAA")
        score.score_goal("BBB")
        score.set_status(s.GameStatus.SECOND_QUARTER)
        score.score_goal("AAA")
        score.set_status(s.GameStatus.THIRD_QUARTER)
        score.score_goal("BBB")
        score.set_status(s.GameStatus.FOURTH_QUARTER)
        score.score_behind("BBB")
        score.set_status(s.GameStatus.FULL_TIME)

        team_scores = score.get_final_score()

        self.assertEqual(team_scores["AAA"].total(), 12)
        self.assertEqual(team_scores["BBB"].total(), 13)