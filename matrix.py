from math import fsum
from status import BallStatus, Possession, FieldStatus

BOUNCE_STATUS = FieldStatus(Possession.IN_CONTENTION, BallStatus.BOUNCE)
STOPPED_STATUS = FieldStatus(Possession.IN_CONTENTION, BallStatus.STOPPED)
THROW_IN_STATUS = FieldStatus(Possession.IN_CONTENTION, BallStatus.THROW_IN)

HOME_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(Possession.HOME_TEAM, BallStatus.OUT_OF_BOUNDS)
HOME_TEAM_FREE_KICK_STATUS = FieldStatus(Possession.HOME_TEAM, BallStatus.FREE_KICK)
HOME_TEAM_MOVING_STATUS = FieldStatus(Possession.HOME_TEAM, BallStatus.MOVING)
HOME_TEAM_BEHIND_STATUS = FieldStatus(Possession.HOME_TEAM, BallStatus.BEHIND)
HOME_TEAM_GOAL_STATUS = FieldStatus(Possession.HOME_TEAM, BallStatus.GOAL)

AWAY_TEAM_OUT_OF_BOUNDS_STATUS = FieldStatus(Possession.AWAY_TEAM, BallStatus.OUT_OF_BOUNDS)
AWAY_TEAM_FREE_KICK_STATUS = FieldStatus(Possession.AWAY_TEAM, BallStatus.FREE_KICK)
AWAY_TEAM_MOVING_STATUS = FieldStatus(Possession.AWAY_TEAM, BallStatus.MOVING)
AWAY_TEAM_BEHIND_STATUS = FieldStatus(Possession.AWAY_TEAM, BallStatus.BEHIND)
AWAY_TEAM_GOAL_STATUS = FieldStatus(Possession.AWAY_TEAM, BallStatus.GOAL)

def prob(base, strength, accuracy, pressure):
    value = base + base * strength + base * accuracy - base * pressure
    return value if value > 0 else 0


def prob_dist(dist, base, strength, accuracy, pressure):
    # Skill probability
    p = prob(base, strength, accuracy, pressure)

    # Distance probability where distance is 1, 2, or 3
    d = 1 - 0.4 * (dist - 1)
    # d = 0.5 + (2 - distance) * 0.3

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

# Each matrix row has a base probability. Certain elements in the matrix have a dynamic quality:
# the probability is modified depending on the skill.
# Each row is then normalised to ensure it adds to 1 (to conform to the Markov property).
# The matrix is stored in a dictionary named the `data` field.
class ZoneMatrix:
    def __init__(self, zone):
        self.zone = zone
        self.data = {}

    @property
    def states(self):
        return list(self.data.keys())

    def row(self, state):
        return self.data[state]

