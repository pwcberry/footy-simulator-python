from enum import Enum, IntEnum
from dataclasses import dataclass

class GameStatus(Enum):
    NOT_STARTED = 0
    FIRST_QUARTER = 1
    QUARTER_TIME = 2
    SECOND_QUARTER = 3
    HALF_TIME = 4
    THIRD_QUARTER = 5
    THREE_QUARTER_TIME = 6
    FOURTH_QUARTER = 7
    FULL_TIME = 8

    def __str__(self):
        if self.name == "QUARTER_TIME":
            return "1/4 Time"
        elif self.name == "HALF_TIME":
            return "1/2 Time"
        elif self.name == "THREE_QUARTER_TIME":
            return "3/4 Time"
        else:
            return self.name.title().replace("_", " ")

class BallStatus(Enum):
    BOUNCE = 0
    STOPPED = 1
    THROW_IN = 2
    OUT_OF_BOUNDS = 3
    FREE_KICK = 4
    MOVING = 5
    BEHIND = 6
    GOAL = 7

class BallDirection(Enum):
    NONE = 0
    FORWARD = 1
    BACKWARD = 2
    LATERAL = 3

class LateralDirection(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2

class Possession(Enum):
    HOME_TEAM = 0
    AWAY_TEAM = 1
    IN_CONTENTION = 2

class FieldZone(Enum):
    RUCK = 0
    FORWARDS = 1
    MID_FIELD = 2
    BACKS = 3   

class AttackDistance(IntEnum):
    GOAL_SQUARE = 1
    TWENTY_METRES = 2
    FIFTY_METRES = 3

@dataclass(frozen=True)
class FieldStatus:
    possession: Possession
    ball_status: BallStatus

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
