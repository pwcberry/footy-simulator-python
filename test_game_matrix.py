import unittest
from unittest.mock import patch
from status import BallDirection, BallStatus, FieldStatus, LateralDirection, Possession
from matrix import HOME_TEAM_MOVING_STATUS, HOME_TEAM_GOAL_STATUS
from data import Skills, Team
from game_matrix import GameMatrix

class TestGameMatrix(unittest.TestCase):
    def setUp(self):
        self.home_team = Team(
            name = "AAA",
            forwards = Skills(0.5, 0.5, 0.5),
            mid_field = Skills(0.5, 0.5, 0.5),
            backs = Skills(0.5, 0.5, 0.5),
            ruck = Skills(0.5, 0.5, 0.5)
        )

        self.away_team = Team(
            name = "BBB",
            forwards = Skills(0.5, 0.5, 0.5),
            mid_field = Skills(0.5, 0.5, 0.5),
            backs = Skills(0.5, 0.5, 0.5),
            ruck = Skills(0.5, 0.5, 0.5)
        )

    def test_next_state_for_midfield(self):
        with patch("numpy.random.default_rng") as mock_fn:
            mock_rng = mock_fn()
            mock_rng.choice.side_effect = [HOME_TEAM_MOVING_STATUS, BallDirection.NONE, LateralDirection.NONE]

            field_status = FieldStatus(Possession.IN_CONTENTION, BallStatus.BOUNCE)
            matrix = GameMatrix(self.home_team, self.away_team)
            new_field_status, new_ball_direction, lateral_direction = matrix.next_state(field_status, 5, BallDirection.NONE)

            self.assertEqual(new_field_status, HOME_TEAM_MOVING_STATUS)
            self.assertEqual(new_ball_direction, BallDirection.NONE)
            self.assertEqual(lateral_direction, LateralDirection.NONE)

    def test_next_state_for_home_team_forwards(self):
        with patch("numpy.random.default_rng") as mock_fn:
            mock_rng = mock_fn()
            mock_rng.choice.side_effect = [HOME_TEAM_GOAL_STATUS, BallDirection.FORWARD, LateralDirection.NONE]

            field_status = FieldStatus(Possession.HOME_TEAM, BallStatus.MOVING)
            matrix = GameMatrix(self.home_team, self.away_team)
            new_field_status, new_ball_direction, lateral_direction = matrix.next_state(field_status, 1, BallDirection.FORWARD)

            self.assertEqual(new_field_status, HOME_TEAM_GOAL_STATUS)
            self.assertEqual(new_ball_direction, BallDirection.FORWARD)
            self.assertEqual(lateral_direction, LateralDirection.NONE)

    def test_next_state_for_home_team_backs(self):
        with patch("numpy.random.default_rng") as mock_fn:
            mock_rng = mock_fn()
            mock_rng.choice.side_effect = [HOME_TEAM_MOVING_STATUS, BallDirection.LATERAL, LateralDirection.RIGHT]

            field_status = FieldStatus(Possession.HOME_TEAM, BallStatus.MOVING)
            matrix = GameMatrix(self.home_team, self.away_team)
            new_field_status, new_ball_direction, lateral_direction = matrix.next_state(field_status, 9, BallDirection.LATERAL)

            self.assertEqual(new_field_status, HOME_TEAM_MOVING_STATUS)
            self.assertEqual(new_ball_direction, BallDirection.LATERAL)
            self.assertEqual(lateral_direction, LateralDirection.RIGHT)


if __name__ == "__main__":
    unittest.main()
