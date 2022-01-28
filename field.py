import math
from random import random
from enum import Enum
from data import Team
from status import BallStatus

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
        self.teams = dict([
            (Possession.HOME_TEAM, home_team),
            (Possession.AWAY_TEAM, away_team)
        ])
        self.position = 5
        self.ball_status = BallStatus.BOUNCE
        self.in_attack = Possession.IN_CONTENTION

    @property
    def in_defence(self):
        if self.in_attack == Possession.IN_CONTENTION:
            return Possession.IN_CONTENTION
        
        return Possession.AWAY_TEAM if self.in_attack == Possession.HOME_TEAM else Possession.HOME_TEAM
    
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
        self.in_attack = Possession.IN_CONTENTION

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
        if self.in_attack == Possession.HOME_TEAM:
            if self.position > 1:
                self.position -= 1
        elif self.in_attack == Possession.AWAY_TEAM:
            if self.position < 9:
                self.position += 1

    def move_backward(self):
        if self.in_attack == Possession.HOME_TEAM:
            if self.position < 9:
                self.position += 1
        elif self.in_attack == Possession.AWAY_TEAM:
            if self.position > 1:
                self.position -= 1

    def workout_ruck_contest(self):
        home_skill = self.teams[Possession.HOME_TEAM].ruck
        away_skill = self.teams[Possession.AWAY_TEAM].ruck

        self.in_attack = get_contest_winner(0.1, 0.45, home_skill.strength, away_skill.strength)

        if self.in_attack != Possession.IN_CONTENTION:
            accuracy_contest = get_contest_winner(0.05, 0.475, home_skill.accuracy, away_skill.accuracy)

            if accuracy_contest != Possession.IN_CONTENTION:
                if accuracy_contest != self.in_attack:
                    self.in_attack = accuracy_contest
                    self.ball_status = BallStatus.STOPPED
                else:
                    self.ball_status = BallStatus.MOVING
            else:
                self.in_attack = Possession.IN_CONTENTION

        if self.in_attack == Possession.IN_CONTENTION:
            if self.ball_status == BallStatus.THROW_IN:
                nbr = random()
                strength_diff = home_skill.strength - away_skill.strength
                upper_limit_for_tussle = 1 - math.sqrt(abs(strength_diff))

                if nbr > upper_limit_for_tussle:
                    self.ball_status = BallStatus.MOVING


    def workout_midfield_contest(self):
        in_attack_skill = self.teams[self.in_attack].mid_field
        in_defense_skill = self.teams[self.in_defence].mid_field
        ball_direction = BallDirection.NONE

        return
        # if self.ball_status == BallStatus.STOPPED:
        #     self.ball_status = get_status_after_stopped_ball()
        # elif self.ball_status == BallStatus.FREE_KICK:
        #     ball_direction = get_ball_direction(0.05, 0.475, in_attack_skill.strength, in_defense_skill.strength)
        #     accuracy_contest = get_contest_winner(0.05, 0.475, in_attack_skill.accuracy, in_defense_skill.accuracy)
        #     # do something here, and I think it's to call an instance method
        #     # to clarify what happens next
        # elif self.ball_status == BallStatus.OUT_OF_BOUNDS:
        #     # is in_attack already switched?
        # else:
        #     # ball is moving!
        #     strength_contest = get_contest_winner(0.05, 0.475, in_attack_skill.strength, in_defense_skill.strength)
        #     # We need to write out some more pseudo-code to ensure the logic is correct
        #     # And I have a suspicion that there's reusable functions to discover

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
