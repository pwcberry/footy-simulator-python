from enum import IntEnum
from .game_score import GameScore
from .status import GameStatus
from .timer import Timer

class GameLogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    ACTION = 4
    SCORE = 8
    QUARTER = 16
    FINAL = 32

class GameLog:
    def __init__(self, output, level = GameLogLevel.ACTION):
        self.output = output
        self.level = level if isinstance(level, GameLogLevel) else GameLogLevel[level]

    def _write_quarter_time(self, status: GameStatus, score: GameScore):
        self.output.write("** {} **\n".format(status))
        self.output.write(score.get_current_score())
        self.output.write("\n")

    def get_short_score(self, score: GameScore):
        scores = [(team, score.total()) for team, score in score.current_scores.items()]
        return "{0} {1}, {2} {3}".format(scores[0][0], scores[0][1], scores[1][0], scores[1][1])

    def log_debug(self, message: str):
        if self.level == GameLogLevel.DEBUG:
            self.output.write("DEBUG : {}\n".format(message))

    def log_info(self, message: str):
        if self.level <= GameLogLevel.INFO:
            self.output.write("INFO  : {}\n".format(message))

    def log_game_status(self, status: GameStatus):
        if self.level <= GameLogLevel.ACTION:
            self.output.write("STATUS: {}\n".format(status))

    def log_action(self, timer: Timer, message: str):
        if self.level <= GameLogLevel.ACTION:
            self.output.write("{0} - {1}\n".format(timer, message))

    def log_goal(self, timer: Timer, team_name: str, score: GameScore):
        if self.level <= GameLogLevel.SCORE:
            self.output.write("{}: GOAL!!: {}\n{}\n".format(timer, team_name, self.get_short_score(score)))

    def log_behind(self, timer: Timer, team_name: str, score: GameScore):
        if self.level <= GameLogLevel.SCORE:
            self.output.write("{}: BEHIND: {}\n{}\n".format(timer, team_name, self.get_short_score(score)))

    def log_quarter_time(self, status: GameStatus, score: GameScore):
        if self.level <= GameLogLevel.QUARTER:
            self._write_quarter_time(status, score)

    def log_final_result(self, score: GameScore):
        if self.level >= GameLogLevel.FINAL:
            self._write_quarter_time(GameStatus.FULL_TIME, score)

        if self.level <= GameLogLevel.FINAL:
            final_score = score.get_final_score()
            team_scores = [(team, score.total()) for team, score in final_score.items()]
            margin = abs(team_scores[0][1] - team_scores[1][1])
            
            if margin > 0:
                winning_team = team_scores[0][0] if team_scores[0][1] > team_scores[1][1] else team_scores[1][0]
                self.output.write("RESULT: {} WON by {} points\n".format(winning_team, margin))
            else:
                self.output.write("RESULT: DRAW\n")
