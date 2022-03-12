import numpy as np
import unittest
from unittest.mock import patch

from .context import afl, data as d, status as s

class TestGameMatrix(unittest.TestCase):
    def setUp(self):
        self.home_team = d.Team(
            name = "AAA",
            forwards = d.Skills(0.5, 0.5, 0.5),
            mid_field = d.Skills(0.5, 0.5, 0.5),
            backs = d.Skills(0.5, 0.5, 0.5),
            ruck = d.Skills(0.5, 0.5, 0.5)
        )

        self.away_team = d.Team(
            name = "BBB",
            forwards = d.Skills(0.5, 0.5, 0.5),
            mid_field = d.Skills(0.5, 0.5, 0.5),
            backs = d.Skills(0.5, 0.5, 0.5),
            ruck = d.Skills(0.5, 0.5, 0.5)
        )

    def set_numpy_side_effect(self, field_status, ball_direction, lateral_direction):
        return [
            np.array([field_status]),
            np.array([ball_direction]),
            np.array([lateral_direction])
        ]

    def test_next_state_for_midfield(self):
        with patch("numpy.random.default_rng") as mock_fn:
            mock_rng = mock_fn()
            mock_rng.choice.side_effect = self.set_numpy_side_effect(s.HOME_TEAM_MOVING_STATUS, s.BallDirection.NONE, s.LateralDirection.NONE)

            field_status = s.FieldStatus(s.Possession.IN_CONTENTION, s.BallStatus.BOUNCE)
            position = afl.Position(x = afl.FIELD_CENTER_X, y = afl.FIELD_CENTER_Y)
            matrix = afl.GameMatrix(self.home_team, self.away_team)
            new_field_status, new_ball_direction, lateral_direction = matrix.next_state(field_status, position, s.BallDirection.NONE)

            self.assertEqual(new_field_status, s.HOME_TEAM_MOVING_STATUS)
            self.assertEqual(new_ball_direction, s.BallDirection.NONE)
            self.assertEqual(lateral_direction, s.LateralDirection.NONE)

    def test_next_state_for_home_team_forwards(self):
        with patch("numpy.random.default_rng") as mock_fn:
            mock_rng = mock_fn()
            mock_rng.choice.side_effect = self.set_numpy_side_effect(s.HOME_TEAM_GOAL_STATUS, s.BallDirection.FORWARD, s.LateralDirection.NONE)

            field_status = afl.FieldStatus(s.Possession.HOME_TEAM, s.BallStatus.MOVING)
            position = afl.Position(x = afl.FIELD_MAX_X, y = afl.FIELD_CENTER_Y)
            matrix = afl.GameMatrix(self.home_team, self.away_team)
            new_field_status, new_ball_direction, lateral_direction = matrix.next_state(field_status, position, s.BallDirection.FORWARD)

            self.assertEqual(new_field_status, s.HOME_TEAM_GOAL_STATUS)
            self.assertEqual(new_ball_direction, s.BallDirection.FORWARD)
            self.assertEqual(lateral_direction, s.LateralDirection.NONE)

    def test_next_state_for_home_team_backs(self):
        with patch("numpy.random.default_rng") as mock_fn:
            mock_rng = mock_fn()
            mock_rng.choice.side_effect = self.set_numpy_side_effect(s.HOME_TEAM_MOVING_STATUS, s.BallDirection.LATERAL, s.LateralDirection.RIGHT)

            field_status = afl.FieldStatus(s.Possession.HOME_TEAM, s.BallStatus.MOVING)
            position = afl.Position(x = afl.FIELD_MIN_X, y = afl.FIELD_CENTER_Y)
            matrix = afl.GameMatrix(self.home_team, self.away_team)
            new_field_status, new_ball_direction, lateral_direction = matrix.next_state(field_status, position, s.BallDirection.LATERAL)

            self.assertEqual(new_field_status, s.HOME_TEAM_MOVING_STATUS)
            self.assertEqual(new_ball_direction, s.BallDirection.LATERAL)
            self.assertEqual(lateral_direction, s.LateralDirection.RIGHT)

if __name__ == "__main__":
    unittest.main()
