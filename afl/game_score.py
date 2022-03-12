from .data import TeamScore
from .status import GameStatus

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
