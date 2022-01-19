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


def prob_dist(dist, base, strength, accuracy, pressure):
    # Skill probability
    p = prob(base, strength, accuracy, pressure)

    # Distance probability
    d = 1 - 0.4 * (dist - 1)

    return p + d * p  


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

class Matrix:
    @property
    def states(self):
        return self.matrix.keys()
