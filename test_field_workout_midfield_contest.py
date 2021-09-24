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

class TestFieldWorkoutMidfieldContest(unittest.TestCase):
    def setUp(self):
        self.home_team = Team(
            name = "AAA",
            forwards = set_default_skills(),
            mid_field = Skills(
                strength = 0.6,
                accuracy = 0.4,
                pressure = 0.5
            ),
            backs = set_default_skills(),
            ruck = set_default_skills(),
            cohesion = 0.8,
            fitness = 0.9
        )
        self.away_team = Team(
            name = "BBB",
            forwards = set_default_skills(),
            mid_field = Skills(
                strength = 0.3,
                accuracy = 0.6,
                pressure = 0.5
            ),
            backs = set_default_skills(),
            ruck = set_default_skills(),
            cohesion = 0.8,
            fitness = 0.9
        )
        self.f = Field(
            self.home_team,
            self.away_team
        )




    
if __name__ == "__main__":
    unittest.main()
