import unittest
from unittest.mock import patch
from field import get_team_in_attack, Contest

class TestFieldTeamInAttack(unittest.TestCase):
    
    def test_should_be_in_contention_when_less_than_minimum(self):
        with patch("field.random", return_value = 0.08):
            status = get_team_in_attack(0.1, 0.5, 0.4, 0.2)
            self.assertEqual(status, Contest.IN_CONTENTION)

    def test_should_be_home_team_when_skills_overlap(self):
        with patch("field.random", return_value = 0.58) as rnd:
            status = get_team_in_attack(0.1, 0.5, 0.6, 0.5)
            self.assertEqual(status, Contest.HOME_TEAM)

            rnd.return_value = 0.71
            status = get_team_in_attack(0.1, 0.5, 0.6, 0.5)
            self.assertEqual(status, Contest.AWAY_TEAM)


    def test_should_be_away_team_when_skills_overlap(self):
        with patch("field.random", return_value = 0.42) as rnd:
            status = get_team_in_attack(0.1, 0.5, 0.5, 0.6)
            self.assertEqual(status, Contest.AWAY_TEAM)

            rnd.return_value = 0.39
            status = get_team_in_attack(0.1, 0.5, 0.5, 0.6)
            self.assertEqual(status, Contest.HOME_TEAM)


    def test_should_be_home_team_when_skills_dont_overlap(self):
        with patch("field.random", return_value = 0.49) as rnd:
            status = get_team_in_attack(0.1, 0.5, 0.5, 0.3)
            self.assertEqual(status, Contest.HOME_TEAM)

            rnd.return_value = 0.05
            status = get_team_in_attack(0.1, 0.5, 0.5, 0.3)
            self.assertEqual(status, Contest.HOME_TEAM)

            rnd.return_value = 0.51     
            status = get_team_in_attack(0.1, 0.5, 0.5, 0.3)
            self.assertEqual(status, Contest.AWAY_TEAM)


    def test_should_be_home_team_when_skills_dont_overlap(self):
        with patch("field.random", return_value = 0.31) as rnd:
            status = get_team_in_attack(0.1, 0.5, 0.3, 0.5)
            self.assertEqual(status, Contest.AWAY_TEAM)

            rnd.return_value = 0.51     
            status = get_team_in_attack(0.1, 0.5, 0.3, 0.5)
            self.assertEqual(status, Contest.AWAY_TEAM)

            rnd.return_value = 0.11   
            status = get_team_in_attack(0.1, 0.5, 0.5, 0.3)
            self.assertEqual(status, Contest.HOME_TEAM)


    def test_should_be_in_contention_when_skills_dont_overlap(self):
        with patch("field.random", return_value = 0.9) as rnd:
            status = get_team_in_attack(0.1, 0.5, 0.4, 0.2)
            self.assertEqual(status, Contest.IN_CONTENTION)

    
if __name__ == "__main__":
    unittest.main()
