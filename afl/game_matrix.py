import numpy
from .status import AttackDistance, BallDirection, LateralDirection, Possession
from .field import FIELD_MAX_X, FIELD_MIN_X
from afl.matrix import BacksDirectionMatrix, BacksZoneMatrix, ForwardsDirectionMatrix, ForwardsZoneMatrix, MidfieldDirectionMatrix, MidFieldZoneMatrix, RuckZoneMatrix

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
            if field_position.x <= 3:
                matrix = self.forwards[field_position.x - FIELD_MIN_X]
                direction_matrix = self.forwards_direction
            elif field_position.x >= 7:
                matrix = self.backs[FIELD_MAX_X - field_position.x]
                direction_matrix = self.backs_direction
            else:
                matrix = self.midfield
                direction_matrix = self.midfield_direction
        else:
            matrix = self.ruck
            direction_matrix = None

        probabilities = matrix.row(field_status)
        arr = self.rng.choice(matrix.states, 1, p = probabilities)
        new_field_status = arr.item(0)

        if direction_matrix != None:
            probabilities = direction_matrix.row(ball_direction, field_status.possession)
            arr = self.rng.choice(direction_matrix.states, 1, p = probabilities)
            new_ball_direction = arr.item(0)
        else:
            new_ball_direction = BallDirection.NONE

        if new_ball_direction == BallDirection.LATERAL:
            arr = self.rng.choice([LateralDirection.LEFT, LateralDirection.RIGHT], 1, p = [0.5, 0.5])
            lateral_direction = arr.item(0)
        else:
            lateral_direction = LateralDirection.NONE

        return (new_field_status, new_ball_direction, lateral_direction)
