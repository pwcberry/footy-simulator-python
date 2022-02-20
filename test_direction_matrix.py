import unittest
from status import BallDirection, FieldZone, Possession
from direction_matrix import DirectionMatrix

class TestDirectionMatrix(unittest.TestCase):
    def setUp(self):
        self.states = [
            BallDirection.NONE, BallDirection.FORWARD, 
            BallDirection.BACKWARD, BallDirection.LATERAL
        ]

    def test_states_returns_expected_list(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        self.assertEqual(len(matrix.states), len(self.states))
        self.assertEqual(matrix.states, self.states)

    def test_row_returns_when_possession_is_in_contention(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        row = matrix.row(BallDirection.NONE, Possession.IN_CONTENTION)
        self.assertEqual(len(self.states), len(row))

    def test_row_raises_error_when_possesion_is_home_team(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        with self.assertRaises(KeyError):
            row = matrix.row(BallDirection.NONE, Possession.HOME_TEAM)

    def test_row_raises_error_when_possesion_is_away_team(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        with self.assertRaises(KeyError):
            row = matrix.row(BallDirection.NONE, Possession.AWAY_TEAM)

    def test_data_shape_is_consistent(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        matrix_states = matrix.states
        count = len(matrix_states)

        for s in matrix_states:
            v = matrix.row(s, Possession.IN_CONTENTION)
            self.assertEqual(len(v), count)

    def test_data_each_row_is_normalised(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)

        for s in matrix.states:
            r = matrix.row(s, Possession.IN_CONTENTION)
            v = sum(r)
            self.assertAlmostEqual(v, 1.0)

    def test_row_first_item_is_1_when_ball_direction_is_none(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        row = matrix.row(BallDirection.NONE, Possession.IN_CONTENTION)
        self.assertEqual(row[0], 1)

    def test_row_first_item_is_1_when_ball_direction_is_forward(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        row = matrix.row(BallDirection.FORWARD, Possession.IN_CONTENTION)
        self.assertEqual(row[0], 1)

    def test_row_first_item_is_1_when_ball_direction_is_backward(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        row = matrix.row(BallDirection.BACKWARD, Possession.IN_CONTENTION)
        self.assertEqual(row[0], 1)

    def test_row_first_item_is_1_when_ball_direction_is_lateral(self):
        matrix = DirectionMatrix(FieldZone.MID_FIELD)
        row = matrix.row(BallDirection.LATERAL, Possession.IN_CONTENTION)
        self.assertEqual(row[0], 1)


if __name__ == "__main__":
    unittest.main()

