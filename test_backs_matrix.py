import unittest
from matrix import *
from data import Skills
from backs_matrix import BacksZoneMatrix
from status import AttackDistance, FieldZone

class TestBacksZoneMatrix(unittest.TestCase):
    def setUp(self):
        self.states = [
            BOUNCE_STATUS, STOPPED_STATUS, THROW_IN_STATUS,
            HOME_TEAM_OUT_OF_BOUNDS_STATUS, HOME_TEAM_FREE_KICK_STATUS, HOME_TEAM_MOVING_STATUS,
            AWAY_TEAM_OUT_OF_BOUNDS_STATUS, AWAY_TEAM_FREE_KICK_STATUS, AWAY_TEAM_MOVING_STATUS,
            AWAY_TEAM_BEHIND_STATUS, AWAY_TEAM_GOAL_STATUS
        ]
        self.home_team = Skills(0.75, 0.625, 0.8)
        self.away_team = Skills(0.8, 0.75, 0.8)

    def test_zone_returns_expected_field_zone(self):
        matrix = BacksZoneMatrix(self.home_team, self.away_team, AttackDistance.TWENTY_METRES)
        self.assertEqual(matrix.zone, FieldZone.BACKS)

    def test_states_returns_expected_list(self):
        matrix = BacksZoneMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)
        self.assertEqual(len(matrix.states), len(self.states))
        self.assertEqual(matrix.states, self.states)

    def test_data_shape_is_consistent(self):
        matrix = BacksZoneMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)
        matrix_states = matrix.states
        count = len(matrix_states)

        for s in matrix_states:
            v = matrix.row(s)
            self.assertEqual(len(v), count)

    def test_data_each_row_is_normalised(self):
        matrix = BacksZoneMatrix(self.home_team, self.away_team, AttackDistance.GOAL_SQUARE)

        for s in matrix.states:
            r = matrix.row(s)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)


if __name__ == "__main__":
    unittest.main()
