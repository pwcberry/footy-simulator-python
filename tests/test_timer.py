import unittest

from .context import Timer

class TestTimer(unittest.TestCase):

    def test_reset(self):
        timer = Timer()
        timer.tick()
        timer.tick()
        timer.tick()

        self.assertNotEqual(timer.seconds, 0)

        timer.reset()

        self.assertEqual(timer.seconds, 0)

    def test_is_end_of_quarter(self):
        timer = Timer()
        timer.minutes = 20

        self.assertTrue(timer.is_end_of_quarter())

    def test_string_representation(self):
        timer = Timer()
        timer.minutes = 19
        timer.seconds = 6

        self.assertEqual(str(timer), "19:06")

if __name__ == "__main__":
    unittest.main()
