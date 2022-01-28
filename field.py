import math
from random import random
from enum import Enum
from data import Team
from status import BallStatus, FieldZone, Possession

class BallDirection(Enum):
    NONE = 0
    FORWARD = 1
    BACKWARD = 2
    LATERAL = 3

def get_contest_winner(min, midpoint, home_skill, away_skill):
    nbr = random()

    if nbr < min:
        return Possession.IN_CONTENTION

    if home_skill + away_skill >= 1:
        diff = home_skill - away_skill
        limit = midpoint + diff
        return Possession.HOME_TEAM if nbr <= limit else Possession.AWAY_TEAM

    counter = 1
    status = Possession.IN_CONTENTION
    min = home_skill + away_skill

    while counter <= 3 and status == Possession.IN_CONTENTION:
        if nbr <= home_skill:
            status = Possession.HOME_TEAM
        elif nbr > home_skill and nbr <= min:
            status = Possession.AWAY_TEAM
        else:
            nbr = random()
            counter += 1
    
    return status

def get_status_after_stopped_ball():
    nbr = random()
    return Status.BOUNCE if nbr < 0.5 else Status.THROW_IN

def get_ball_direction(min, midpoint, attack_strength, defense_strength):
    nbr = random()

    if nbr < min:
        return BallDirection.LATERAL

    if attack_strength + defense_strength >= 1:
        diff = attack_strength - defense_strength
        limit = midpoint + diff
        return BallDirection.FORWARD if nbr <= limit else BallDirection.BACKWARD

    return BallDirection.FORWARD if attack_strength > defense_strength else BallDirection.BACKWARD            

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

