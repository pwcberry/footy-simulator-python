import unittest
from unittest.mock import patch
from data import Team, Skills
from status import BallStatus
from field import Field, Contest

def set_default_skills():
    return Skills(
        strength = 0.5,
        accuracy = 0.5,
        pressure = 0.5
    )

class TestFieldWorkoutRuckContest(unittest.TestCase):
    def setUp(self):
        self.home_team = Team(
            name = "AAA",
            forwards = set_default_skills(),
            mid_field = set_default_skills(),
            backs = set_default_skills(),
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
            forwards = set_default_skills(),
            mid_field = set_default_skills(),
            backs = set_default_skills(),
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

    def test_should_be_home_team_in_attack(self):
        with patch("field.random", return_value = 0.2):
            self.f.workout_ruck_contest()
            self.assertEqual(self.f.in_attack, Contest.HOME_TEAM)
            self.assertEqual(self.f.ball_status, BallStatus.MOVING)

    def test_should_be_away_team_in_attack(self):
        with patch("field.random", return_value = 0.7):
            self.f.workout_ruck_contest()
            self.assertEqual(self.f.in_attack, Contest.AWAY_TEAM)
            self.assertEqual(self.f.ball_status, BallStatus.MOVING)        

    def test_should_be_away_team_in_attack_and_ball_stopped(self):
        with patch("field.random", return_value = 0.6):
            self.f.workout_ruck_contest()
            self.assertEqual(self.f.in_attack, Contest.AWAY_TEAM)
            self.assertEqual(self.f.ball_status, BallStatus.STOPPED)

    
if __name__ == "__main__":
    unittest.main()
