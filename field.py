import math
from random import random
from enum import Enum
from data import Team
from status import BallStatus


class Contest(Enum):
    HOME_TEAM = 0
    AWAY_TEAM = 1
    IN_CONTENTION = 2

class BallPosition(Enum):
    FULL_FOWARD = 1
    POCKET_FORWARD = 2
    HALF_FORWARD = 3
    MID_FIELD_FORWARD = 4
    CENTRE = 5
    MID_FIELD_BACK = 6
    HALF_BACK = 7
    POCKET_BACK = 8
    FULL_BACK = 9

def get_team_in_attack(min, midpoint, home_skill, away_skill):
    nbr = random()

    if nbr < min:
        return Contest.IN_CONTENTION

    if home_skill + away_skill >= 1:
        diff = home_skill - away_skill
        limit = midpoint + diff
        return Contest.HOME_TEAM if nbr <= limit else Contest.AWAY_TEAM

    counter = 1
    status = Contest.IN_CONTENTION
    min = home_skill + away_skill

    while counter <= 3 and status == Contest.IN_CONTENTION:
        if nbr <= home_skill:
            status = Contest.HOME_TEAM
        elif nbr > home_skill and nbr <= min:
            status = Contest.AWAY_TEAM
        else:
            nbr = random()
            counter += 1
    
    return status


class Field:
    def __init__(self, home_team: Team, away_team: Team):
        self.teams = dict([
            (Contest.HOME_TEAM, home_team),
            (Contest.AWAY_TEAM, away_team)
        ])
        self.position = 5
        self.ball_status = BallStatus.BOUNCE
        self.in_attack = Contest.IN_CONTENTION

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
        self.in_attack = Contest.IN_CONTENTION

    def get_active_home_team_skill(self):
        if self.ball_status == BallStatus.BOUNCE or self.ball_status == BallStatus.THROW_IN:
            return "ruck"
        elif self.position in [1, 2, 3]:
            return "forwards"
        elif self.position in [4, 5, 6]:
            return "mid_field"
        else:
            return "backs"

    def move_forward(self):
        if self.in_attack == Contest.HOME_TEAM:
            if self.position > 1:
                self.position -= 1
        elif self.in_attack == Contest.AWAY_TEAM:
            if self.position < 9:
                self.position += 1

    def move_backward(self):
        if self.in_attack == Contest.HOME_TEAM:
            if self.position < 9:
                self.position += 1
        elif self.in_attack == Contest.AWAY_TEAM:
            if self.position > 1:
                self.position -= 1

    def workout_ruck_contest(self):
        home_skill = self.teams[Contest.HOME_TEAM].ruck
        away_skill = self.teams[Contest.AWAY_TEAM].ruck

        self.in_attack = get_team_in_attack(0.1, 0.45, home_skill.strength, away_skill.strength)

        if self.in_attack != Contest.IN_CONTENTION:
            accuracy_contest = get_team_in_attack(0.05, 0.475, home_skill.accuracy, away_skill.accuracy)

            if accuracy_contest != Contest.IN_CONTENTION:
                if accuracy_contest != self.in_attack:
                    self.in_attack = accuracy_contest
                    self.ball_status = BallStatus.STOPPED
                else:
                    self.ball_status = BallStatus.MOVING
            else:
                self.in_attack = Contest.IN_CONTENTION

        if self.in_attack == Contest.IN_CONTENTION:
            if self.ball_status == BallStatus.THROW_IN:
                nbr = random()
                strength_diff = home_skill.strength - away_skill.strength
                upper_limit_for_tussle = 1 - math.sqrt(abs(strength_diff))

                if nbr > upper_limit_for_tussle:
                    self.ball_status = BallStatus.MOVING

    def workout_midfield_contest(self):
        return

    def workout_forward_contest(self):
        return

    def workout_back_contest(self):
        return

    def generate_snapshot(self):
        active_skill = self.get_active_home_team_skill()

        if active_skill == "ruck":
            self.workout_ruck_contest()
        elif active_skill == "mid_field":
            self.workout_midfield_contest()
        elif active_skill == "forward":
            self.workout_forward_contest()
        else:
            self.workout_back_contest()
        
        team_in_attack = self.teams[self.in_attack]
        return self.ball_status, team_in_attack
