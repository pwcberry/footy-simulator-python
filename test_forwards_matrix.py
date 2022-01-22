import unittest
from matrix import *
from data import Skills
from forwards_matrix import ForwardsMatrix
from status import AttackDistance

class TestForwardsMatrix(unittest.TestCase):
    def setUp(self):
        self.states = [
            RUCK_BOUNCE_STATUS, RUCK_STOPPED_STATUS, RUCK_THROW_IN_STATUS,
            FORWARDS_THROW_IN_STATUS, FORWARDS_HOME_TEAM_STOPPED_STATUS, 
            FORWARDS_HOME_TEAM_OUT_OF_BOUNDS_STATUS, FORWARDS_HOME_TEAM_FREE_KICK_STATUS,
            FORWARDS_HOME_TEAM_MOVING_STATUS, FORWARDS_HOME_TEAM_BEHIND_STATUS,
            FORWARDS_HOME_TEAM_GOAL_STATUS, FORWARDS_AWAY_TEAM_STOPPED_STATUS,
            FORWARDS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, FORWARDS_AWAY_TEAM_FREE_KICK_STATUS,
            FORWARDS_AWAY_TEAM_MOVING_STATUS
        ]
        self.home_team = Skills(0.75, 0.625, 0.8)
        self.away_team = Skills(0.8, 0.75, 0.8)

    def test_states_returns_expected_list(self):
        matrix = ForwardsMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)
        self.assertEqual(len(matrix.states), len(self.states))
        self.assertEqual(matrix.states, self.states)

    def test_data_shape_is_consistent(self):
        matrix = ForwardsMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)
        matrix_states = matrix.states
        count = len(matrix_states)

        for s in matrix_states:
            v = matrix.row(s)
            self.assertEqual(len(v), count)

    def test_data_each_row_is_normalised(self):
        matrix = ForwardsMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)

        for s in matrix.states:
            r = matrix.row(s)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)


if __name__ == "__main__":
    unittest.main()
