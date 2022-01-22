import unittest
from matrix import *
from data import Skills
from midfield_matrix import MidFieldMatrix

class TestMidFieldMatrix(unittest.TestCase):
    def setUp(self):
        self.states = [
            RUCK_BOUNCE_STATUS, RUCK_STOPPED_STATUS, RUCK_THROW_IN_STATUS,
            MID_FIELD_THROW_IN_STATUS, MID_FIELD_HOME_TEAM_STOPPED_STATUS,
            MID_FIELD_HOME_TEAM_OUT_OF_BOUNDS_STATUS, MID_FIELD_HOME_TEAM_FREE_KICK_STATUS,
            MID_FIELD_HOME_TEAM_MOVING_STATUS, MID_FIELD_AWAY_TEAM_STOPPED_STATUS,
            MID_FIELD_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, MID_FIELD_AWAY_TEAM_FREE_KICK_STATUS,
            MID_FIELD_AWAY_TEAM_MOVING_STATUS
        ]
        self.home_team = Skills(0.75, 0.625, 0.8)
        self.away_team = Skills(0.8, 0.75, 0.8)

    def test_states_returns_expected_list(self):
        matrix = MidFieldMatrix(self.home_team, self.away_team)
        self.assertEqual(len(matrix.states), len(self.states))
        self.assertEqual(matrix.states, self.states)

    def test_data_shape_is_consistent(self):
        matrix = MidFieldMatrix(self.home_team, self.away_team)
        matrix_states = matrix.states
        count = len(matrix_states)

        for s in matrix_states:
            v = matrix.row(s)
            self.assertEqual(len(v), count)

    def test_data_each_row_is_normalised(self):
        matrix = MidFieldMatrix(self.home_team, self.away_team)

        for s in matrix.states:
            r = matrix.row(s)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)


if __name__ == "__main__":
    unittest.main()
