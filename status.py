from enum import Enum
from dataclasses import dataclass
from data import TeamScore

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

class BallStatus(Enum):
    BOUNCE = 0
    STOPPED = 1
    THROW_IN = 2
    OUT_OF_BOUNDS = 3
    FREE_KICK = 4
    MOVING = 5
    BEHIND = 6
    GOAL = 7

class Possession(Enum):
    HOME_TEAM = 0
    AWAY_TEAM = 1
    IN_CONTENTION = 2

class FieldArea(Enum):
    RUCK = 0
    FORWARDS = 1
    MID_FIELD = 2
    BACKS = 3   

@dataclass(frozen=True)
class FieldStatus:
    field_area: FieldArea
    possession: Possession
    ball_status: BallStatus

GAME_TICKS_PER_MINUTE = 10
MINUTES_PER_QUARTER = 20

class Timer:
    minutes = 0
    seconds = 0

    def __init__(self):
        self.reset()

    def tick(self):
        self.seconds += 60 // GAME_TICKS_PER_MINUTE

        if self.seconds >= 60:
            self.minutes += 1
            self.seconds = 0

        if self.minutes > MINUTES_PER_QUARTER:
            self.minutes = MINUTES_PER_QUARTER

    def is_end_of_quarter(self):
        return self.minutes >= MINUTES_PER_QUARTER

    def current_time(self):
        return self.minutes, self.seconds

    def reset(self):
        self.minutes = 0
        self.seconds = 0

    def __repr__(self):
        return "Timer({0:02}, {1:02})".format(self.minutes, self.seconds)

    def __str__(self):
        return "{0:02}:{1:02}".format(self.minutes, self.seconds)


class GameScore:
    def __init__(self, home_team_name, away_team_name):
        self.quarter_scores = dict([
            (home_team_name, []),
            (away_team_name, [])
        ])
        self.current_scores = dict([
            (home_team_name, TeamScore()),
            (away_team_name, TeamScore())
        ])
        self.quarter = 0

    def score_goal(self, team_name):
        score = self.current_scores[team_name]
        score.goals += 1

    def score_behind(self, team_name):
        score = self.current_scores[team_name]
        score.behinds += 1

    def set_status(self, status):
        if status == GameStatus.FIRST_QUARTER:
            self.quarter = 1
        elif status == GameStatus.SECOND_QUARTER:
            self.quarter = 2
            self._set_quarter_time_score()
        elif status == GameStatus.THIRD_QUARTER:
            self.quarter = 3
            self._set_quarter_time_score()
        elif status == GameStatus.FOURTH_QUARTER:
            self.quarter = 4
            self._set_quarter_time_score()
        elif status == GameStatus.FULL_TIME:
            self.quarter = 5
            self._set_quarter_time_score()

    def get_current_score(self):
        s = ""
        for key, value in self.current_scores.items():
            s += "{0}: {1}\n".format(key, value)

        return s

    def get_final_score(self):
        if self.quarter != 5:
            raise RuntimeError("Attempted to retrieve final score when the game has not reached full time")

        return dict(
            [(key, self.quarter_scores[key][3]) for key in iter(self.quarter_scores)]
        )

    def _set_quarter_time_score(self):
        for key in iter(self.current_scores):
            self.quarter_scores[key].append(self.current_scores[key])

