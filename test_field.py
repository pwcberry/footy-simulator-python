import unittest
from field import *
from data import Team, Skills
from status import BallStatus, FieldZone, LateralDirection, Possession

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

        self.assertEqual(f.position, Position(FIELD_CENTER_X, FIELD_CENTER_Y))
        self.assertEqual(f.ball_status, BallStatus.BOUNCE)
        self.assertEqual(f.possession, Possession.IN_CONTENTION)
        self.assertEqual(f.teams[0], self.team_a)
        self.assertEqual(f.teams[1], self.team_b)

    def test_set_position(self):
        f = Field(self.team_a, self.team_b)
        f.set_position(Position(4, 3))
        self.assertEqual(f.position.x, 4)
        self.assertEqual(f.position.y, 3)

    def test_set_position_x_less_than_minimum(self):
        f = Field(self.team_a, self.team_b)
        f.set_position(Position(-1, 3))
        self.assertEqual(f.position.x, FIELD_MIN_X)

    def test_set_position_x_greater_than_maximum(self):
        f = Field(self.team_a, self.team_b)
        f.set_position(Position(10, 3))
        self.assertEqual(f.position.x, FIELD_MAX_X)

    def test_set_position_x_less_than_minimum(self):
        f = Field(self.team_a, self.team_b)
        f.set_position(Position(3, 0))
        self.assertEqual(f.position.y, FIELD_MIN_Y)

    def test_set_position_x_greater_than_maximum(self):
        f = Field(self.team_a, self.team_b)
        f.set_position(Position(3, 6))
        self.assertEqual(f.position.y, FIELD_MAX_Y)

    def test_centre_ball(self):
        f = Field(self.team_a, self.team_b)
        f.centre_ball()
        self.assertEqual(f.position, Position(FIELD_CENTER_X, FIELD_CENTER_Y))
        self.assertEqual(f.ball_status, BallStatus.BOUNCE)
        self.assertEqual(f.possession, Possession.IN_CONTENTION)

    def test_get_field_zone_at_bounce(self):
        f = Field(self.team_a, self.team_b)
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.RUCK)

    def test_get_field_zone_when_moving(self):
        f = Field(self.team_a, self.team_b)
        f.ball_status = BallStatus.MOVING

        f.set_position(Position(1, 1))
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.FORWARDS)

        f.set_position(Position(3, 2))
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.FORWARDS)

        f.set_position(Position(4, 3))
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.MID_FIELD)

        f.set_position(Position(6, 4))
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.MID_FIELD)

        f.set_position(Position(7, 5))
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.BACKS)

        f.set_position(Position(9, 4))
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.BACKS)

    def test_get_field_zone_when_ball_is_thrown_in(self):
        f = Field(self.team_a, self.team_b)
        f.ball_status = BallStatus.THROW_IN
        f.set_position(Position(6, 1))
        zone = f.get_field_zone()
        self.assertEqual(zone, FieldZone.RUCK)

    def test_field_status_returns_possession_and_ball_status(self):
        f = Field(self.team_a, self.team_b)
        fs = f.field_status
        self.assertEqual(fs.possession, Possession.IN_CONTENTION)
        self.assertEqual(fs.ball_status, BallStatus.BOUNCE)

    # Move forwards

    def test_move_forward_when_possession_is_home_team_and_in_field_center(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.move_forward()
        self.assertEqual(f.position.x, FIELD_CENTER_X - 1)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_forward_when_possession_is_home_team_and_at_forward_limit(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.set_position(Position(FIELD_MIN_X, FIELD_CENTER_Y))
        f.move_forward()
        self.assertEqual(f.position.x, FIELD_MIN_X)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_forward_when_possession_is_home_team_and_in_back_field(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.set_position(Position(FIELD_MAX_X, FIELD_CENTER_Y))
        f.move_forward()
        self.assertEqual(f.position.x, FIELD_MAX_X - 1)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_forward_when_possession_is_away_team_and_in_field_center(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.move_forward()
        self.assertEqual(f.position.x, FIELD_CENTER_X + 1)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_forward_when_possession_is_away_team_and_at_forward_limit(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.set_position(Position(FIELD_MAX_X, FIELD_CENTER_Y))
        f.move_forward()
        self.assertEqual(f.position.x, FIELD_MAX_X)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_forward_when_possession_is_away_team_and_in_back_field(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.set_position(Position(FIELD_MIN_X, FIELD_CENTER_Y))
        f.move_forward()
        self.assertEqual(f.position.x, FIELD_MIN_X + 1)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    ## Move backwards

    def test_move_backward_when_possession_is_home_team_and_in_field_center(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.move_backward()
        self.assertEqual(f.position.x, FIELD_CENTER_X + 1)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_backward_when_possession_is_home_team_and_at_back_limit(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.set_position(Position(FIELD_MAX_X, FIELD_CENTER_Y))
        f.move_backward()
        self.assertEqual(f.position.x, FIELD_MAX_X)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_backward_when_possession_is_home_team_and_in_forward_field(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.set_position(Position(FIELD_MIN_X, FIELD_CENTER_Y))
        f.move_backward()
        self.assertEqual(f.position.x, FIELD_MIN_X + 1)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_backward_when_possession_is_away_team_and_in_field_center(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.move_backward()
        self.assertEqual(f.position.x, FIELD_CENTER_X - 1)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_backward_when_possession_is_away_team_and_at_back_limit(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.set_position(Position(FIELD_MIN_X, FIELD_CENTER_Y))
        f.move_backward()
        self.assertEqual(f.position.x, FIELD_MIN_X)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    def test_move_backward_when_possession_is_away_team_and_in_forward_field(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.set_position(Position(FIELD_MAX_X, FIELD_CENTER_Y))
        f.move_backward()
        self.assertEqual(f.position.x, FIELD_MAX_X - 1)
        self.assertEqual(f.position.y, FIELD_CENTER_Y)

    # Move laterally - HOME_TEAM

    def test_move_laterally_when_possession_is_home_team_and_in_field_center_and_move_left(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.move_laterally(LateralDirection.LEFT)
        self.assertEqual(f.position.x, FIELD_CENTER_X)
        self.assertEqual(f.position.y, FIELD_CENTER_Y + 1)

    def test_move_laterally_when_possession_is_home_team_and_in_field_center_and_move_right(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.move_laterally(LateralDirection.RIGHT)
        self.assertEqual(f.position.x, FIELD_CENTER_X)
        self.assertEqual(f.position.y, FIELD_CENTER_Y - 1)
        
    def test_move_laterally_when_possession_is_home_team_and_at_left_side_and_move_left(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.set_position(Position(FIELD_CENTER_X, FIELD_MAX_Y))
        f.move_laterally(LateralDirection.LEFT)
        self.assertEqual(f.position.x, FIELD_CENTER_X)
        self.assertEqual(f.position.y, FIELD_MAX_Y)

    def test_move_laterally_when_possession_is_home_team_and_at_right_side_and_move_right(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.HOME_TEAM
        f.set_position(Position(FIELD_CENTER_X, FIELD_MIN_Y))
        f.move_laterally(LateralDirection.RIGHT)
        self.assertEqual(f.position.x, FIELD_CENTER_X)
        self.assertEqual(f.position.y, FIELD_MIN_Y)

    # Move laterally - AWAY_TEAM

    def test_move_laterally_when_possession_is_away_team_and_in_field_center_and_move_left(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.move_laterally(LateralDirection.LEFT)
        self.assertEqual(f.position.x, FIELD_CENTER_X)
        self.assertEqual(f.position.y, FIELD_CENTER_Y - 1)

    def test_move_laterally_when_possession_is_away_team_and_in_field_center_and_move_right(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.move_laterally(LateralDirection.RIGHT)
        self.assertEqual(f.position.x, FIELD_CENTER_X)
        self.assertEqual(f.position.y, FIELD_CENTER_Y + 1)
        
    def test_move_laterally_when_possession_is_away_team_and_at_left_side_and_move_left(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.set_position(Position(FIELD_CENTER_X, FIELD_MIN_Y))
        f.move_laterally(LateralDirection.LEFT)
        self.assertEqual(f.position.x, FIELD_CENTER_X)
        self.assertEqual(f.position.y, FIELD_MIN_Y)

    def test_move_laterally_when_possession_is_away_team_and_at_right_side_and_move_right(self):
        f = Field(self.team_a, self.team_b)
        f.possession = Possession.AWAY_TEAM
        f.set_position(Position(FIELD_CENTER_X, FIELD_MAX_Y))
        f.move_laterally(LateralDirection.RIGHT)
        self.assertEqual(f.position.x, FIELD_CENTER_X)
        self.assertEqual(f.position.y, FIELD_MAX_Y)
        

if __name__ == "__main__":
    unittest.main()
