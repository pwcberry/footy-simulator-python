import unittest
from matrix import *
from data import Skills
from backs_matrix import BacksMatrix
from status import AttackDistance

class TestBacksMatrix(unittest.TestCase):
    def setUp(self):
        self.states = [
            RUCK_BOUNCE_STATUS, RUCK_STOPPED_STATUS, RUCK_THROW_IN_STATUS,
            BACKS_THROW_IN_STATUS, BACKS_HOME_TEAM_STOPPED_STATUS, 
            BACKS_HOME_TEAM_OUT_OF_BOUNDS_STATUS, BACKS_HOME_TEAM_FREE_KICK_STATUS,
            BACKS_HOME_TEAM_MOVING_STATUS, BACKS_AWAY_TEAM_STOPPED_STATUS,
            BACKS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, BACKS_AWAY_TEAM_FREE_KICK_STATUS,
            BACKS_AWAY_TEAM_MOVING_STATUS, BACKS_AWAY_TEAM_BEHIND_STATUS,
            BACKS_AWAY_TEAM_GOAL_STATUS
        ]
        self.home_team = Skills(0.75, 0.625, 0.8)
        self.away_team = Skills(0.8, 0.75, 0.8)

    def test_states_returns_expected_list(self):
        matrix = BacksMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)
        self.assertEqual(len(matrix.states), len(self.states))
        self.assertEqual(matrix.states, self.states)

    def test_data_shape_is_consistent(self):
        matrix = BacksMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)
        matrix_states = matrix.states
        count = len(matrix_states)

        for s in matrix_states:
            v = matrix.row(s)
            self.assertEqual(len(v), count)

    def test_data_each_row_is_normalised(self):
        matrix = BacksMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)

        for s in matrix.states:
            r = matrix.row(s)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)


if __name__ == "__main__":
    unittest.main()
