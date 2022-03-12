import unittest

from ..context import data as d, matrix as m, status as s

class TestMidFieldZoneMatrix(unittest.TestCase):
    def setUp(self):
        self.states = [
            s.STOPPED_STATUS, s.THROW_IN_STATUS,
            s.HOME_TEAM_OUT_OF_BOUNDS_STATUS, s.HOME_TEAM_FREE_KICK_STATUS, s.HOME_TEAM_MOVING_STATUS, 
            s.AWAY_TEAM_OUT_OF_BOUNDS_STATUS, s.AWAY_TEAM_FREE_KICK_STATUS, s.AWAY_TEAM_MOVING_STATUS
        ]
        self.home_team = d.Skills(0.75, 0.625, 0.8)
        self.away_team = d.Skills(0.8, 0.75, 0.8)

    def test_zone_returns_expected_field_zone(self):
        matrix = m.MidFieldZoneMatrix(self.home_team, self.away_team)
        self.assertEqual(matrix.zone, s.FieldZone.MID_FIELD)

    def test_states_returns_expected_list(self):
        matrix = m.MidFieldZoneMatrix(self.home_team, self.away_team)
        self.assertEqual(len(matrix.states), len(self.states))
        self.assertEqual(matrix.states, self.states)

    def test_data_shape_is_consistent(self):
        matrix = m.MidFieldZoneMatrix(self.home_team, self.away_team)
        matrix_states = matrix.states
        count = len(matrix_states)

        for st in matrix_states:
            v = matrix.row(st)
            self.assertEqual(len(v), count)

    def test_data_each_row_is_normalised(self):
        matrix = m.MidFieldZoneMatrix(self.home_team, self.away_team)

        for st in matrix.states:
            r = matrix.row(st)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)


if __name__ == "__main__":
    unittest.main()