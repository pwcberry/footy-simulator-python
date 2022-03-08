from collections import namedtuple
from status import BallStatus, FieldZone, FieldStatus, LateralDirection, Possession  

FIELD_MIN_X = 1
FIELD_MAX_X = 9
FIELD_MIN_Y = 1
FIELD_MAX_Y = 5
FIELD_CENTER_X = 5
FIELD_CENTER_Y = 3

Position = namedtuple("Position", ["x", "y"])

class Field:
    def __init__(self, home_team, away_team):
        self.teams = (home_team, away_team)
        self.centre_ball()
    
    @property
    def field_status(self):
        return FieldStatus(self.possession, self.ball_status)

    @field_status.setter
    def field_status(self, value):
        self.possession = value.possession
        self.ball_status = value.ball_status

    def set_position(self, new_position):
        if new_position.x < FIELD_MIN_X:
            new_position = Position(FIELD_MIN_X, new_position.y)
        elif new_position.x > FIELD_MAX_X:
            new_position = Position(FIELD_MAX_X, new_position.y)

        if new_position.y < FIELD_MIN_Y:
            new_position = Position(new_position.x, FIELD_MIN_Y)
        elif new_position.y > FIELD_MAX_Y:
            new_position = Position(new_position.x, FIELD_MAX_Y)

        self.position = new_position
            
    def centre_ball(self):
        self.position = Position(FIELD_CENTER_X, FIELD_CENTER_Y)
        self.ball_status = BallStatus.BOUNCE
        self.possession = Possession.IN_CONTENTION

    def get_field_zone(self):
        if self.ball_status == BallStatus.BOUNCE or self.ball_status == BallStatus.THROW_IN:
            return FieldZone.RUCK
        elif self.position.x in [1, 2, 3]:
            return FieldZone.FORWARDS
        elif self.position.x in [4, 5, 6]:
            return FieldZone.MID_FIELD
        else:
            return FieldZone.BACKS

    def move_forward(self):
        if self.possession == Possession.HOME_TEAM:
            if self.position.x > FIELD_MIN_X:
                self.position = Position(self.position.x - 1, self.position.y)
        elif self.possession == Possession.AWAY_TEAM:
            if self.position.x < FIELD_MAX_X:
                self.position = Position(self.position.x + 1, self.position.y)

    def move_backward(self):
        if self.possession == Possession.HOME_TEAM:
            if self.position.x < FIELD_MAX_X:
                self.position = Position(self.position.x + 1, self.position.y)
        elif self.possession == Possession.AWAY_TEAM:
            if self.position.x > FIELD_MIN_X:
                self.position = Position(self.position.x - 1, self.position.y)

    def move_laterally(self, direction):
        if self.possession == Possession.HOME_TEAM:
            if (direction == LateralDirection.LEFT) and (self.position.y < FIELD_MAX_Y):
                self.position = Position(self.position.x, self.position.y + 1)
            elif (direction == LateralDirection.RIGHT) and (self.position.y > FIELD_MIN_Y):
                self.position = Position(self.position.x, self.position.y - 1)
        elif self.possession == Possession.AWAY_TEAM:
            if (direction == LateralDirection.LEFT) and (self.position.y > FIELD_MIN_Y):
                self.position = Position(self.position.x, self.position.y - 1)
            elif (direction == LateralDirection.RIGHT) and (self.position.y < FIELD_MAX_Y):
                self.position = Position(self.position.x, self.position.y + 1)

    def switch_possession(self):
        if self.possession == Possession.HOME_TEAM:
            self.possession = Possession.AWAY_TEAM
        elif self.possession == Possession.AWAY_TEAM:
            self.possession = Possession.HOME_TEAM
    
