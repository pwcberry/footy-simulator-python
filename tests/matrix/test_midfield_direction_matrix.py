import unittest

from ..context import data as d, matrix as m, status as s

class TestMidfieldDirectionMatrix(unittest.TestCase):
    def setUp(self):
        self.states = [
            s.BallDirection.NONE, s.BallDirection.FORWARD, 
            s.BallDirection.BACKWARD, s.BallDirection.LATERAL
        ]
        self.home_team = d.Skills(0.75, 0.625, 0.8)
        self.away_team = d.Skills(0.8, 0.75, 0.8)

    def test_zone_returns_expected_field_zone(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)
        self.assertEqual(matrix.zone, s.FieldZone.MID_FIELD)

    def test_states_returns_expected_list(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)
        self.assertEqual(len(matrix.states), len(self.states))
        self.assertEqual(matrix.states, self.states)

    def test_row_returns_when_possession_is_in_contention(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)
        row = matrix.row (s.BallDirection.NONE, s.Possession.IN_CONTENTION)
        self.assertEqual(len(self.states), len(row))

    def test_row_returns_when_possession_is_home_team(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)
        row = matrix.row (s.BallDirection.NONE, s.Possession.HOME_TEAM)
        self.assertEqual(len(self.states), len(row))

    def test_row_returns_when_possession_is_away_team(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)
        row = matrix.row (s.BallDirection.NONE, s.Possession.AWAY_TEAM)
        self.assertEqual(len(self.states), len(row))

    def test_data_shape_is_consistent_when_possession_is_home_team(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)
        matrix_states = matrix.states
        count = len(matrix_states)        

        for st in matrix_states:
            v = matrix.row(st, s.Possession.HOME_TEAM)
            self.assertEqual(len(v), count)

    def test_data_shape_is_consistent_when_possession_is_away_team(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)
        matrix_states = matrix.states
        count = len(matrix_states)

        for st in matrix_states:
            v = matrix.row(st, s.Possession.AWAY_TEAM)
            self.assertEqual(len(v), count)

    def test_data_each_row_is_normalised_when_possession_is_home_team(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)

        for st in matrix.states:
            r = matrix.row(st, s.Possession.HOME_TEAM)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)

    def test_data_each_row_is_normalised_when_possession_is_away_team(self):
        matrix = m.MidfieldDirectionMatrix(self.home_team, self.away_team)

        for st in matrix.states:
            r = matrix.row(st, s.Possession.AWAY_TEAM)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)


if __name__ == "__main__":
    unittest.main()
