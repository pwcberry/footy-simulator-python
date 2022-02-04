from random import random
from status import BallStatus, FieldZone, FieldStatus, Possession  

class Field:
    def __init__(self, home_team, away_team):
        self.teams = (home_team, away_team)
        self.position = 5
        self.ball_status = BallStatus.BOUNCE
        self.possession = Possession.IN_CONTENTION
    
    @property
    def get_field_status(self):
        return FieldStatus(self.possession, self.ball_status)

    def set_position(self, new_position):
        if new_position < 1:
            self.position = 1
        elif new_position > 9:
            self.position = 9
        else:
            self.position = new_position
            
    def centre_ball(self):
        self.position = 5
        self.ball_status = BallStatus.BOUNCE
        self.possession = Possession.IN_CONTENTION

    def get_field_zone(self):
        if self.ball_status == BallStatus.BOUNCE or self.ball_status == BallStatus.THROW_IN:
            return FieldZone.RUCK
        elif self.position in [1, 2, 3]:
            return FieldZone.FORWARDS
        elif self.position in [4, 5, 6]:
            return FieldZone.MID_FIELD
        else:
            return FieldZone.BACKS

    def move_forward(self):
        if self.possession == Possession.HOME_TEAM:
            if self.position > 1:
                self.position -= 1
        elif self.possession == Possession.AWAY_TEAM:
            if self.position < 9:
                self.position += 1

    def move_backward(self):
        if self.possession == Possession.HOME_TEAM:
            if self.position < 9:
                self.position += 1
        elif self.possession == Possession.AWAY_TEAM:
            if self.position > 1:
                self.position -= 1

