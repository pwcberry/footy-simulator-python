import sys
from random import random
from collections import namedtuple
from data import Team
from status import BallStatus, GameScore, GameStatus, Timer
from field import Field
from logger import GameLog


# Their rating for defence: in preventing scores and moving the ball to the mid-field
# Their rating for mid-field: retaining the ball and moving to the forward line
# Their rating for forwards: ability take possession and score
# Their rating for team cohesion
# Their rating for team (physical) health
# Their rating for goal kicking accuracy
# Ratings are a float between 0 and 1

# TODO:
# Workout the rules of the simulation
# Does health decrease with ticks, is it random, or is it a factor that affects the other ratings?

# Examples of Markov chains: https://en.wikipedia.org/wiki/Examples_of_Markov_chains
# Use Matrices to work out probabilities and the next state (result of the contest)
# Other references:
# - https://en.wikipedia.org/wiki/Stochastic_matrix (Transition Matrix)
# - https://en.wikipedia.org/wiki/Monte_Carlo_method


MAX_X = 2
MAX_Y = 6

Position = namedtuple("Position", ["x", "y"])


class Game:
    def __init__(self, home_team: Team, away_team: Team, log_output = sys.stdout):
        self.field = Field(home_team, away_team)
        self.status = GameStatus.NOT_STARTED
        self.score = GameScore(home_team.name, away_team.name)
        self.logger = GameLog(log_output)
        self.timer = Timer()

    def play_quarter(self):
        if self.status == GameStatus.FULL_TIME:
            self.logger.log_message(self.timer, "Game is finished!")
            return
        elif self.status == GameStatus.NOT_STARTED:
            self.status = GameStatus.FIRST_QUARTER
        elif self.status == GameStatus.FIRST_QUARTER:
            self.status = GameStatus.SECOND_QUARTER
        elif self.status == GameStatus.SECOND_QUARTER:
            self.status = GameStatus.THIRD_QUARTER
        elif self.status == GameStatus.THIRD_QUARTER:
            self.status = GameStatus.FOURTH_QUARTER

        self.timer.reset()
        self.score.set_status(self.status)
        self.logger.log_status(self.status)
        self.field.centre_ball()
        self.play()

        # End of quarter
        if self.status == GameStatus.FIRST_QUARTER:
            self.status = GameStatus.QUARTER_TIME
        elif self.status == GameStatus.SECOND_QUARTER:
            self.status = GameStatus.HALF_TIME
        elif self.status == GameStatus.THIRD_QUARTER:
            self.status = GameStatus.THREE_QUARTER_TIME
        elif self.status == GameStatus.FOURTH_QUARTER:
            self.status = GameStatus.FULL_TIME

        self.logger.log_status(self.status)
        self.logger.log_full_score(self.score)          

        if self.status == GameStatus.FULL_TIME:
            self.log_result()

    def play(self):
        while not self.timer.is_end_of_quarter():
            self.timer.tick()
            ball_status, team_in_attack = self.field.generate_snapshot()

            if ball_status == BallStatus.GOAL:
                self.score_goal(team_in_attack)
            elif ball_status == BallStatus.BEHIND:
                self.score_behind(team_in_attack)


    def score_goal(self, team):
        self.score.score_goal(team.name)
        self.logger.log_message(self.timer, "{}: GOAL!".format(team.name))
        self.logger.log_short_score(self.timer, self.score)
        self.reset_field()

    def score_behind(self, team):
        self.score.score_behind(team.name)
        self.logger.log_message(self.timer, "{}: Behind".format(team.name))

    def log_result(self):
        team_scores = [(team, score.total()) for team, score in self.score.get_final_score()]
        margin = abs(team_scores[0][1] - team_scores[1][1])
        
        if margin > 0:
            winning_team = team_scores[0][0] if team_scores[0][1] > team_scores[1][1] else team_scores[1][0]
            result = "\n{} WON by {} points\n".format(winning_team, margin)
            self.logger.log_message(self.timer, result)
        else:
            self.logger.log_message(self.timer, "\nDRAW\n")
    
