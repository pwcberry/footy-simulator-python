import random
from math import fsum
from status import BallStatus, Possession, FieldArea, FieldStatus

RUCK_BOUNCE_STATUS = FieldStatus(FieldArea.RUCK, BallStatus.BOUNCE, Possession.IN_CONTENTION)
RUCK_STOPPED_STATUS = FieldStatus(FieldArea.RUCK, BallStatus.STOPPED, Possession.IN_CONTENTION)
RUCK_THROW_IN_STATUS = FieldStatus(FieldArea.RUCK, BallStatus.THROW_IN, Possession.IN_CONTENTION)

MID_FIELD_THROW_IN_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.IN_CONTENTION, BallStatus.THROW_IN)
MID_FIELD_HOME_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.STOPPED)
MID_FIELD_HOME_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.OUT_OF_BOUNDS)
MID_FIELD_HOME_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.FREE_KICK)
MID_FIELD_HOME_TEAM_MOVING_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.MOVING)

MID_FIELD_AWAY_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.STOPPED)
MID_FIELD_AWAY_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.OUT_OF_BOUNDS)
MID_FIELD_AWAY_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.FREE_KICK)
MID_FIELD_AWAY_TEAM_MOVING_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.MOVING)

FORWARDS_THROW_IN_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.IN_CONTENTION, BallStatus.THROW_IN)
FORWARDS_HOME_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.STOPPED)
FORWARDS_HOME_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.OUT_OF_BOUNDS)
FORWARDS_HOME_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.FREE_KICK)
FORWARDS_HOME_TEAM_MOVING_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.MOVING)
FORWARDS_HOME_TEAM_BEHIND_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.BEHIND)
FORWARDS_HOME_TEAM_GOAL_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.GOAL)

FORWARDS_AWAY_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.STOPPED)
FORWARDS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.OUT_OF_BOUNDS)
FORWARDS_AWAY_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.FREE_KICK)
FORWARDS_AWAY_TEAM_MOVING_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.MOVING)

BACKS_THROW_IN_STATUS = FieldStatus(FieldArea.BACKS, Possession.IN_CONTENTION, BallStatus.THROW_IN)
BACKS_HOME_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.STOPPED)
BACKS_HOME_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.OUT_OF_BOUNDS)
BACKS_HOME_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.FREE_KICK)
BACKS_HOME_TEAM_MOVING_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.MOVING)

BACKS_AWAY_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.BACKS, Possession.AWAY_TEAM, BallStatus.STOPPED)
BACKS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.BACKS, Possession.AWAY_TEAM, BallStatus.OUT_OF_BOUNDS)
BACKS_AWAY_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.BACKS, Possession.AWAY_TEAM, BallStatus.FREE_KICK)
BACKS_AWAY_TEAM_MOVING_STATUS = FieldStatus(FieldArea.BACKS, Possession.AWAY_TEAM, BallStatus.MOVING)
BACKS_AWAY_TEAM_BEHIND_STATUS = FieldStatus(FieldArea.BACKS, Possession.AWAY_TEAM, BallStatus.BEHIND)
BACKS_AWAY_TEAM_GOAL_STATUS = FieldStatus(FieldArea.BACKS, Possession.AWAY_TEAM, BallStatus.GOAL)

"""
Each matrix row has a base probability. Certain elements in the matrix have a dynamic quality:
the probability is modified depending on the skill.

Each row is then normalised to ensure it adds to 1 (to conform to the Markov property).
"""


def prob(base, strength, accuracy, pressure):
    value = base + base * strength + base * accuracy - base * pressure
    return value if value > 0 else 0


def normalise(row, dynamic_indexes):   
    prob_sum = fsum(row)

    while prob_sum != 1.0:
        diff = 1.0 - prob_sum
        adjustment = diff / len(dynamic_indexes)

        for i in dynamic_indexes:
            row[i] += adjustment
            if row[i] <= 1e-4:
                row[i] = 0

        prob_sum = fsum(row)
    
    return row


class MidFieldMatrix:
    def __init__(self, home_team_skill, away_team_skill):
        hst = home_team_skill.strength
        ha = home_team_skill.accuracy
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        aa = away_team_skill.accuracy
        ap = away_team_skill.pressure

        self.matrix = dict(
            (RUCK_BOUNCE_STATUS, 
                normalise([
                    0, 0.05, 0.05, 0.01, 
                    prob(0.05, hst, 0, ap), prob(0.02, 0, -ha, -ap), 0.01, prob(0.2, hst, ha, ap), 
                    prob(0.05, ast, 0, hp), prob(0.02, 0, -aa, -hp), 0.1, prob(0.2, ast, aa, hp)
                ], [4, 5, 7, 8, 9, 11])
            ),
            (RUCK_STOPPED_STATUS, [0.9, 0.03, 0.07, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (RUCK_THROW_IN_STATUS, 
                normalise([
                    0, 0.05, 0, 0.08,
                    prob(0.06, hst, 0, ap), prob(0.01, 0, -ha, -ap), 0.01, prob(0.25, hst, ha, ap),
                    prob(0.06, ast, 0, hp), prob(0.01, 0, -aa, -hp), 0.01, prob(0.25, ast, aa, hp)
                ], [4, 5, 7, 8, 9, 11]),
            (MID_FIELD_THROW_IN_STATUS, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            (MID_FIELD_HOME_TEAM_STOPPED_STATUS,
                normalise([
                    0, 0, 0, 0.01,
                    prob(0.1, hst, 0, ap), 0, prob(0.05, hst, 0, 0), prob(0.44, hst, ha, ap),
                    prob(0.08, ast, 0, hp), 0, prob(0.02, 0, 0, -ap), prob(0.02, ast, 0, -ap)
                ]), [4, 6, 7, 8, 10, 11]),
            (MID_FIELD_HOME_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
            (MID_FIELD_HOME_TEAM_FREE_KICK_STATUS,
                normalise([
                    0, 0, 0, 0, 
                    prob(0.05, 0, -ha, -hp), prob(0.05, 0, -ha, -ap), prob(0.01, 0, 0, -hp), prob(0.55, hst, ha, ap),
                    prob(0.08, 0, -ha, -ap), 0, prob(0.015, 0, 0, -ap), 0
                ]), [4, 5, 6, 7, 8, 10]),
            (MID_FIELD_HOME_TEAM_MOVING_STATUS,
                normalise([
                    0, 0, 0, prob(0.025, 0, -ha, -ap),
                    prob(0.03, 0, -aa, -ap), prob(0.025, 0, -ha, -ap), prob(0.04, hst, 0, -hp), prob(0.5, hst, ha, ap),
                    prob(0.03, 0, -ha, -ap), prob(0.025, 0, -aa, -hp), prob(0.03, ast, 0, -ap), 0
                ]), [3, 4, 5, 6, 7, 8, 9, 10]),
            (MID_FIELD_AWAY_TEAM_STOPPED_STATUS,
                normalise([
                    0, 0, 0, 0.01,
                    prob(0.08, hst, 0, ap), 0, prob(0.02, 0, 0, -hp), prob(0.02, hst, 0, hp), 
                    prob(0.1, ast, 0, hp), 0, prob(0.05, ast, 0, 0), prob(0.44, ast, aa, hp)
                ]), [4, 6, 7, 8, 10, 11]),
            (MID_FIELD_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
            (MID_FIELD_AWAY_TEAM_FREE_KICK_STATUS, 
                normalise([
                    0, 0, 0, 0,
                    prob(0.08, 0, -aa, -hp), 0, prob(0.015, 0, 0, -hp), 0,
                    prob(0.05, 0, -aa, -ap), prob(0.05, 0, -aa, hp), prob(0.01, 0, 0, -ap), prob(0.55, ast, aa, hp)
                ]), [4, 6, 8, 9, 10, 11]),
            (MID_FIELD_AWAY_TEAM_MOVING_STATUS, 
                normalise([
                    0, 0, 0, prob(0.025, 0, -aa, -hp),
                    prob(0.03, 0, -aa, -hp), prob(0.025, 0, -ha, -ap), prob(0.03, hst, 0, -hp), 0,
                    prob(0.03, 0, -ha, -ap), prob(0.025, 0, -aa, -hp), prob(0.04, ast, 0, -hp), prob(0.5, ast, aa, hp)
                ]), [3, 4, 5, 6, 8, 9, 10, 11])
            )
        )

    @property
    def states(self):
        return self.matrix.keys()

class ForwardMatrix:
    def __init__(self, home_team_skill, away_team_skill, distance):
        hst = home_team_skill.strength
        ha = home_team_skill.accuracy
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        aa = away_team_skill.accuracy
        ap = away_team_skill.pressure

        # Distance probability where distance is 1, 2, or 3
        dp = 0.5 + (2 - distance) * 0.3


        self.matrix = dict(
            (FORWARDS_THROW_IN_STATUS, [], [])
            (FORWARDS_HOME_TEAM_STOPPED_STATUS, [], [])
            (FORWARDS_HOME_TEAM_OUT_OF_BOUNDS_STATUS, [], []),
            (FORWARDS_HOME_TEAM_FREE_KICK_STATUS, [], []),
            (FORWARDS_HOME_TEAM_MOVING_STATUS, [], []),
            (FORWARDS_HOME_TEAM_BEHIND_STATUS, [], []),
            (FORWARDS_HOME_TEAM_GOAL_STATUS, [], []),
            (FORWARDS_AWAY_TEAM_STOPPED_STATUS, [], []),
            (FORWARDS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, [], []),
            (FORWARDS_AWAY_TEAM_FREE_KICK_STATUS, [], []),
            (FORWARDS_AWAY_TEAM_MOVING_STATUS, [], [])
        )
  
    @property
    def states(self):
        return self.matrix.keys()

class BacksMatrix:
    def __init__(self, home_team_skill, away_team_skill, distance):
        hst = home_team_skill.strength
        ha = home_team_skill.accuracy
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        aa = away_team_skill.accuracy
        ap = away_team_skill.pressure

        # Distance probability where distance is 1, 2, or 3
        dp = 0.5 + (2 - distance) * 0.3

        self.matrix = dict(
            (BACKS_THROW_IN_STATUS, [], []),
            (BACKS_HOME_TEAM_STOPPED_STATUS, [], []),
            (BACKS_HOME_TEAM_OUT_OF_BOUNDS_STATUS, [], []),
            (BACKS_HOME_TEAM_FREE_KICK_STATUS, [], []),
            (BACKS_HOME_TEAM_MOVING_STATUS, [], []),
            (BACKS_AWAY_TEAM_STOPPED_STATUS, [], []),
            (BACKS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, [], []),
            (BACKS_AWAY_TEAM_FREE_KICK_STATUS, [], []),
            (BACKS_AWAY_TEAM_MOVING_STATUS, [], []),
            (BACKS_AWAY_TEAM_BEHIND_STATUS, [], []),
            (BACKS_AWAY_TEAM_GOAL_STATUS, [], [])
        )
  
    @property
    def states(self):
        return self.matrix.keys()
