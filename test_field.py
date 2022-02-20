import unittest
from field import Field
from data import Team, Skills
from status import BallStatus, FieldZone, Possession

class TestField(unittest.TestCase):
    def setUp(self):
        self.team_a = Team(
            # name
            "AAA", 

            # forwards
            Skills(0.5, 0.5, 0.5), 

            # mid_field
            Skills(0.5, 0.5, 0.5), 

            # backs
            Skills(0.5, 0.5, 0.5), 

            # ruck
            Skills(0.5, 0.5, 0.5),
        )
        self.team_b = Team("BBB", 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5), 
            Skills(0.5, 0.5, 0.5),
        )

    def test_init(self):
        f = Field(self.team_a, self.team_b)

        self.assertEqual(f.position, 5)
        self.assertEqual(f.ball_status, BallStatus.BOUNCE)
        self.assertEqual(f.teams[0], self.team_a)
        self.assertEqual(f.teams[1], self.team_b)
        self.assertEqual(f.possession, Possession.IN_CONTENTION)

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
        self.assertEqual(f.possession, Possession.IN_CONTENTION)

    def test_get_field_zone_at_bounce(self):
        f = Field(self.team_a, self.team_b)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.RUCK)

    def test_get_field_zone_when_moving(self):
        f = Field(self.team_a, self.team_b)
        f.ball_status = BallStatus.MOVING

        f.set_position(1)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.FORWARDS)

        f.set_position(3)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.FORWARDS)

        f.set_position(4)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.MID_FIELD)

        f.set_position(6)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.MID_FIELD)

        f.set_position(7)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.BACKS)

        f.set_position(9)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.BACKS)

    def test_get_field_zone_when_ball_is_thrown_in(self):
        f = Field(self.team_a, self.team_b)
        f.ball_status = BallStatus.THROW_IN
        f.set_position(6)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.RUCK)



    
if __name__ == "__main__":
    unittest.main()
