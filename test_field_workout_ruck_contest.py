import unittest
from unittest.mock import patch
from data import Team, Skills
from status import BallStatus
from field import Field, Contest

class TestFieldWorkoutRuckContest(unittest.TestCase):
    def setUp(self):
        self.home_team = Team(
            name = "AAA",
            forwards = Skills(
                strength = 0.5,
                accuracy = 0.5,
                pressure = 0.5
            ),
            mid_field = Skills(
                strength = 0.5,
                accuracy = 0.5,
                pressure = 0.5
            ),
            backs = Skills(
                strength = 0.5,
                accuracy = 0.5,
                pressure = 0.5
            ),
            ruck = Skills(
                strength = 0.6,
                accuracy = 0.4,
                pressure = 0.5
            ),
            cohesion = 0.8,
            fitness = 0.9
        )
        self.away_team = Team(
            name = "BBB",
            forwards = Skills(
                strength = 0.5,
                accuracy = 0.5,
                pressure = 0.5
            ),
            mid_field = Skills(
                strength = 0.5,
                accuracy = 0.5,
                pressure = 0.5
            ),
            backs = Skills(
                strength = 0.5,
                accuracy = 0.5,
                pressure = 0.5
            ),
            ruck = Skills(
                strength = 0.3,
                accuracy = 0.6,
                pressure = 0.5
            ),
            cohesion = 0.8,
            fitness = 0.9
        )
        self.f = Field(
            self.home_team,
            self.away_team
        )
        

    def test_should_be_in_contention_and_throw_in(self):
        with patch("field.random", return_value = 0.09):
            self.f.ball_status = BallStatus.THROW_IN
            self.f.workout_ruck_contest()
            self.assertEqual(self.f.ball_status, BallStatus.THROW_IN)

    def test_should_be_in_contention_and_bounce(self):
        with patch("field.random", return_value = 0.09):
            self.f.workout_ruck_contest()
            self.assertEqual(self.f.ball_status, BallStatus.BOUNCE)




    
if __name__ == "__main__":
    unittest.main()
