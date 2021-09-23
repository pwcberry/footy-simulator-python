import unittest
from field import Contest, Field
from data import Team, Skills
from status import BallStatus

class TestField(unittest.TestCase):
    def setUp(self):
        self.team_a = Team("AAA", 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5),
            0.5,
            0.8
        )
        self.team_b = Team("BBB", 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5),
            0.5,
            0.8
        )

    def test_init(self):
        f = Field(self.team_a, self.team_b)

        self.assertEqual(f.position, 5)
        self.assertEqual(f.ball_status, BallStatus.BOUNCE)
        self.assertEqual(f.teams[0], self.team_a)
        self.assertEqual(f.teams[1], self.team_b)
        self.assertEqual(f.in_attack, Contest.IN_CONTENTION )

    def test_set_position(self):
        f = Field(self.team_a, self.team_b)
        f.set_position(4)
        self.assertEqual(f.position, 4)

    def test_set_position_less_than_minimum(self):
        f = Field(self.team_a, self.team_b)
        f.set_position(-1)
        self.assertEqual(f.position, 1)

    def test_set_position_greater_than_maximum(self):
        f = Field(self.team_a, self.team_b)
        f.set_position(10)
        self.assertEqual(f.position, 9)

    def test_centre_ball(self):
        f = Field(self.team_a, self.team_b)
        f.centre_ball()
        self.assertEqual(f.position, 5)
        self.assertEqual(f.ball_status, BallStatus.BOUNCE)
        self.assertEqual(f.in_attack, Contest.IN_CONTENTION)

    def test_get_active_skill_at_bounce(self):
        f = Field(self.team_a, self.team_b)

        skill = f.get_active_home_team_skill()
        self.assertEqual(skill, "ruck")

    def test_get_active_skill_when_moving(self):
        f = Field(self.team_a, self.team_b)
        f.ball_status = BallStatus.MOVING

        f.set_position(1)
        skill = f.get_active_home_team_skill()
        self.assertEqual(skill, "forwards")

        f.set_position(3)
        skill = f.get_active_home_team_skill()
        self.assertEqual(skill, "forwards")

        f.set_position(4)
        skill = f.get_active_home_team_skill()
        self.assertEqual(skill, "mid_field")

        f.set_position(6)
        skill = f.get_active_home_team_skill()
        self.assertEqual(skill, "mid_field")

        f.set_position(7)
        skill = f.get_active_home_team_skill()
        self.assertEqual(skill, "backs")

        f.set_position(9)
        skill = f.get_active_home_team_skill()
        self.assertEqual(skill, "backs")

    def test_get_active_skill_when_ball_is_thrown_in(self):
        f = Field(self.team_a, self.team_b)
        f.ball_status = BallStatus.THROW_IN
        f.set_position(6)

        skill = f.get_active_home_team_skill()

        self.assertEqual(skill, "ruck")



    
if __name__ == "__main__":
    unittest.main()
