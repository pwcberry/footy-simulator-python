import unittest
from matrix import prob, normalise

class TestMatrixProbFunction(unittest.TestCase):

    def test_returns_base_value_with_zero_inputs(self):
        strength = 0
        accuracy = 0
        pressure = 0
        value = prob(0.2, strength, accuracy, pressure)
        self.assertEqual(value, 0.2)

    def test_returns_value_adjusted_for_strength(self):
        strength = 0.1
        accuracy = 0
        pressure = 0
        value = prob(0.2, strength, accuracy, pressure)

        # rounding errors
        self.assertAlmostEqual(value, 0.22)

    def test_returns_value_adjusted_for_accuracy(self):
        strength = 0
        accuracy = 0.2
        pressure = 0
        value = prob(0.2, strength, accuracy, pressure)

        # rounding errors
        self.assertAlmostEqual(value, 0.24)

    def test_returns_value_adjusted_for_pressure(self):
        strength = 0
        accuracy = 0
        pressure = 0.25
        value = prob(0.2, strength, accuracy, pressure)

        # rounding errors
        self.assertAlmostEqual(value, 0.15)


    def test_returns_value_adjusted_for_strength_and_accuracy(self):
        strength = 0.1
        accuracy = 0.2
        pressure = 0.0
        value = prob(0.2, strength, accuracy, pressure)

        # rounding errors
        self.assertAlmostEqual(value, 0.26)


    def test_returns_value_adjusted_for_strength_and_pressure(self):
        strength = 0.1
        accuracy = 0.0
        pressure = 0.25
        value = prob(0.2, strength, accuracy, pressure)

        # rounding errors
        self.assertAlmostEqual(value, 0.17)

    def test_returns_value_adjusted_for_accuracy_and_pressure(self):
        strength = 0.0
        accuracy = 0.2
        pressure = 0.25
        value = prob(0.2, strength, accuracy, pressure)

        # rounding errors
        self.assertAlmostEqual(value, 0.19)

    def test_returns_value_adjusted_for_all_inputs(self):
        strength = 0.1
        accuracy = 0.2
        pressure = 0.25
        value = prob(0.2, strength, accuracy, pressure)

        # rounding errors
        self.assertAlmostEqual(value, 0.21)                


class TestMatrixNormaliseFunction(unittest.TestCase):

    def test_vector_is_unchanged_when_sum_is_one_and_no_dynamic_indexes(self):
        vector = [0.9, 0.025, 0.075, 0, 0]
        result = normalise(vector, [])
        self.assertEqual(vector, result)

    def test_vector_is_changed_when_sum_is_greater_than_one_with_dynamic_index(self):
        vector = [0.7, 0.025, 0.075, 0.15, 0]
        dynamic_indexes = [3, 4]
        result = normalise(vector, dynamic_indexes)

        # rounding errors
        self.assertAlmostEqual(result[3], 0.175)
        self.assertAlmostEqual(result[4], 0.025)

    def test_vector_is_changed_when_sum_is_less_than_one_with_dynamic_index(self):
        vector = [0.7, 0.025, 0.075, 0.2, 0.25]
        dynamic_indexes = [3, 4]
        result = normalise(vector, dynamic_indexes)

        # rounding errors
        self.assertAlmostEqual(result[3], 0.075)
        self.assertAlmostEqual(result[4], 0.125)

    def test_vector_is_changed_when_sum_is_greater_than_one_with_large_dynamic_index(self):
        vector = [0, 0.05, 0.05, 0.07, 0, 0.01, 0.09, 0.38, 0.065, 0, 0.01, 0.1, 0.32]
        dynamic_indexes = [7, 3, 4, 8, 12]
        result = normalise(vector, dynamic_indexes)

        # rounding errors
        self.assertAlmostEqual(result[3], 0.03375)
        self.assertAlmostEqual(result[4], 0)
        self.assertAlmostEqual(result[7], 0.34375)
        self.assertAlmostEqual(result[8], 0.02875)
        self.assertAlmostEqual(result[12], 0.28375)


if __name__ == "__main__":
    unittest.main()
