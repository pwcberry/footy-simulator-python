import unittest
from data import Skills
from status import BallDirection, FieldZone, Possession
from forwards_direction_matrix import ForwardsDirectionMatrix

class TestForwardsDirectionMatrix(unittest.TestCase):
    def setUp(self):
        self.states = [
            BallDirection.NONE, BallDirection.FORWARD, 
            BallDirection.BACKWARD, BallDirection.LATERAL
        ]
        self.home_team = Skills(0.75, 0.625, 0.8)
        self.away_team = Skills(0.8, 0.75, 0.8)

    def test_zone_returns_expected_field_zone(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)
        self.assertEqual(matrix.zone, FieldZone.FORWARDS)

    def test_states_returns_expected_list(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)
        self.assertEqual(len(matrix.states), len(self.states))
        self.assertEqual(matrix.states, self.states)

    def test_row_returns_when_possession_is_in_contention(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)
        row = matrix.row(BallDirection.NONE, Possession.IN_CONTENTION)
        self.assertEqual(len(self.states), len(row))

    def test_row_returns_when_possession_is_home_team(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)
        row = matrix.row(BallDirection.NONE, Possession.HOME_TEAM)
        self.assertEqual(len(self.states), len(row))

    def test_row_returns_when_possession_is_away_team(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)
        row = matrix.row(BallDirection.NONE, Possession.AWAY_TEAM)
        self.assertEqual(len(self.states), len(row))

    def test_data_shape_is_consistent_when_possession_is_home_team(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)
        matrix_states = matrix.states
        count = len(matrix_states)        

        for s in matrix_states:
            v = matrix.row(s, Possession.HOME_TEAM)
            self.assertEqual(len(v), count)

    def test_data_shape_is_consistent_when_possession_is_away_team(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)
        matrix_states = matrix.states
        count = len(matrix_states)        

        for s in matrix_states:
            v = matrix.row(s, Possession.AWAY_TEAM)
            self.assertEqual(len(v), count)

    def test_data_each_row_is_normalised_when_possession_is_home_team(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)

        for s in matrix.states:
            r = matrix.row(s, Possession.HOME_TEAM)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)

    def test_data_each_row_is_normalised_when_possession_is_away_team(self):
        matrix = ForwardsDirectionMatrix(self.home_team, self.away_team)

        for s in matrix.states:
            r = matrix.row(s, Possession.AWAY_TEAM)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)


if __name__ == "__main__":
    unittest.main()
