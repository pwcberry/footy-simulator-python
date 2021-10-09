import random
from status import BallStatus, Possession, FieldArea, FieldStatus

RUCK_BOUNCE_STATUS = FieldStatus(FieldArea.RUCK, BallStatus.BOUNCE, Possession.IN_CONTENTION)
RUCK_STOPPED_STATUS = FieldStatus(FieldArea.RUCK, BallStatus.STOPPED, Possession.IN_CONTENTION)
RUCK_THROW_IN_STATUS = FieldStatus(FieldArea.RUCK, BallStatus.THROW_IN, Possession.IN_CONTENTION)

MID_FIELD_HOME_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.STOPPED)
MID_FIELD_HOME_TEAM_THROW_IN_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.THROW_IN)
MID_FIELD_HOME_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.OUT_OF_BOUNDS)
MID_FIELD_HOME_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.FREE_KICK)
MID_FIELD_HOME_TEAM_MOVING_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.HOME_TEAM, BallStatus.MOVING)

MID_FIELD_AWAY_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.STOPPED)
MID_FIELD_AWAY_TEAM_THROW_IN_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.THROW_IN)
MID_FIELD_AWAY_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.OUT_OF_BOUNDS)
MID_FIELD_AWAY_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.FREE_KICK)
MID_FIELD_AWAY_TEAM_MOVING_STATUS = FieldStatus(FieldArea.MID_FIELD, Possession.AWAY_TEAM, BallStatus.MOVING)

FORWARDS_HOME_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.STOPPED)
FORWARDS_HOME_TEAM_THROW_IN_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.THROW_IN)
FORWARDS_HOME_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.OUT_OF_BOUNDS)
FORWARDS_HOME_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.FREE_KICK)
FORWARDS_HOME_TEAM_MOVING_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.MOVING)
FORWARDS_HOME_TEAM_BEHIND_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.BEHIND)
FORWARDS_HOME_TEAM_GOAL_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.HOME_TEAM, BallStatus.GOAL)

FORWARDS_AWAY_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.STOPPED)
FORWARDS_AWAY_TEAM_THROW_IN_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.THROW_IN)
FORWARDS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.OUT_OF_BOUNDS)
FORWARDS_AWAY_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.FREE_KICK)
FORWARDS_AWAY_TEAM_MOVING_STATUS = FieldStatus(FieldArea.FORWARDS, Possession.AWAY_TEAM, BallStatus.MOVING)

BACKS_HOME_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.STOPPED)
BACKS_HOME_TEAM_THROW_IN_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.THROW_IN)
BACKS_HOME_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.OUT_OF_BOUNDS)
BACKS_HOME_TEAM_FREE_KICK_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.FREE_KICK)
BACKS_HOME_TEAM_MOVING_STATUS = FieldStatus(FieldArea.BACKS, Possession.HOME_TEAM, BallStatus.MOVING)

BACKS_AWAY_TEAM_STOPPED_STATUS = FieldStatus(FieldArea.BACKS, Possession.AWAY_TEAM, BallStatus.STOPPED)
BACKS_AWAY_TEAM_THROW_IN_STATUS = FieldStatus(FieldArea.BACKS, Possession.AWAY_TEAM, BallStatus.THROW_IN)
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
    return base + base * strength + base * accuracy + base * pressure


def normalise(row, dynamic_indexes):
    prob_sum = sum(row)

    diff = prob_sum - 1 if prob_sum < 1 else 1 - prob_sum
    adjustment = diff / len(dynamic_indexes)

    for i in dynamic_indexes:
        row[i] += adjustment

    # Check the row now sums to 1
    # If not, choose a dynamic element at random to bring up the difference
    prob_sum = sum(row)
    if prob_sum != 1:
        diff = prob_sum - 1 if prob_sum < 1 else 1 - prob_sum
        idx = random.choice(dynamic_indexes)
        row[idx] += diff
    
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
                normalise([0, 0.05, 0.05, prob(0.05, 0, ha, 0), 0, 0.01, 0.09, prob(0.2, hst, ha, ap), prob(0.05, 0, aa, 0), 0, 0.01, 0.1, prob(0.2, ast, aa, hp)], [3, 7, 8, 13])
            ),
            (RUCK_STOPPED_STATUS, [0.9, 0.03, 0.07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (RUCK_THROW_IN_STATUS, [0, 0.05, 0]),
            (MID_FIELD_HOME_TEAM_STOPPED_STATUS, []),
            (MID_FIELD_HOME_TEAM_THROW_IN_STATUS, []),
            (MID_FIELD_HOME_TEAM_OUT_OF_BOUNDS_STATUS, []),
            (MID_FIELD_HOME_TEAM_FREE_KICK_STATUS, []),
            (MID_FIELD_HOME_TEAM_MOVING_STATUS, []),
            (MID_FIELD_AWAY_TEAM_STOPPED_STATUS, []),
            (MID_FIELD_AWAY_TEAM_THROW_IN_STATUS, []),
            (MID_FIELD_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, []),
            (MID_FIELD_AWAY_TEAM_FREE_KICK_STATUS, []),
            (MID_FIELD_AWAY_TEAM_MOVING_STATUS, [])
        )





