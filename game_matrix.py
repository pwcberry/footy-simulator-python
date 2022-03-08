from random import random
from status import AttackDistance, BallDirection, LateralDirection, Possession
from ruck_matrix import RuckZoneMatrix
from backs_matrix import BacksZoneMatrix
from backs_direction_matrix import BacksDirectionMatrix
from midfield_matrix import MidFieldZoneMatrix
from midfield_direction_matrix import MidfieldDirectionMatrix
from forwards_matrix import ForwardsZoneMatrix
from forwards_direction_matrix import ForwardsDirectionMatrix
from field import FIELD_MAX_X, FIELD_MIN_X
import numpy

class GameMatrix:
    def __init__(self, home_team, away_team):
        self.ruck = RuckZoneMatrix(home_team.ruck, away_team.ruck)
        self.backs = [
            BacksZoneMatrix(home_team.backs, away_team.backs, AttackDistance.GOAL_SQUARE),
            BacksZoneMatrix(home_team.backs, away_team.backs, AttackDistance.TWENTY_METRES),
            BacksZoneMatrix(home_team.backs, away_team.backs, AttackDistance.FIFTY_METRES)
        ]
        self.backs_direction = BacksDirectionMatrix(home_team.backs, away_team.backs)
        self.midfield = MidFieldZoneMatrix(home_team.mid_field, away_team.mid_field)
        self.midfield_direction = MidfieldDirectionMatrix(home_team.mid_field, away_team.mid_field)
        self.forwards = [
            ForwardsZoneMatrix(home_team.forwards, away_team.forwards, AttackDistance.GOAL_SQUARE),
            ForwardsZoneMatrix(home_team.forwards, away_team.forwards, AttackDistance.TWENTY_METRES),
            ForwardsZoneMatrix(home_team.forwards, away_team.forwards, AttackDistance.FIFTY_METRES)
        ]
        self.forwards_direction = ForwardsDirectionMatrix(home_team.forwards, away_team.forwards)
        self.rng = numpy.random.default_rng()

    def next_state(self, field_status, field_position, ball_direction):
        if field_status.possession != Possession.IN_CONTENTION:
            if field_position <= 3:
                matrix = self.forwards[field_position - FIELD_MIN_X]
                direction_matrix = self.forwards_direction
            elif field_position >= 7:
                matrix = self.backs[FIELD_MAX_X - field_position]
                direction_matrix = self.backs_direction
            else:
                matrix = self.midfield
                direction_matrix = self.midfield_direction
        else:
            matrix = self.ruck
            direction_matrix = None

        probabilities = matrix.row(field_status)
        new_field_status = self.rng.choice(matrix.states, 1, p = probabilities)

        if direction_matrix != None:
            probabilities = direction_matrix.row(ball_direction, field_status.possession)
            new_ball_direction = self.rng.choice(matrix.states, 1, p = probabilities)
        else:
            new_ball_direction = BallDirection.NONE

        if new_ball_direction == BallDirection.LATERAL:
            lateral_direction = self.rng.choice([LateralDirection.LEFT, LateralDirection.RIGHT], 1, p = [0.5, 0.5])
        else:
            lateral_direction = LateralDirection.NONE

        return (new_field_status, new_ball_direction, lateral_direction)
