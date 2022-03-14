import sys
import afl
from .field import Field
from .game_score import GameScore
from .status import *
from .logger import GameLog

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

class Game:
    def __init__(self, home_team, away_team, log_output = sys.stdout):
        self.field = Field(home_team, away_team)
        self.status = GameStatus.NOT_STARTED
        self.score = GameScore(home_team.name, away_team.name)
        self.logger = GameLog(log_output)
        self.timer = afl.timer.Timer()
        self.game_matrix = afl.game_matrix.GameMatrix(home_team, away_team)
        self.home_team = home_team
        self.away_team = away_team
        self.ball_direction = BallDirection.NONE

    @property
    def team_in_attack(self):
        if self.field.possession == Possession.HOME_TEAM:
            return self.home_team
        elif self.field.possession == Possession.AWAY_TEAM:
            return self.away_team
        else:
            return None


    def play_quarter(self):
        if self.status == GameStatus.FULL_TIME:
            self.logger.log_message(self.timer, "Game is finished!")
            return
        elif self.status == GameStatus.NOT_STARTED:
            self.status = GameStatus.FIRST_QUARTER
        elif self.status == GameStatus.QUARTER_TIME:
            self.status = GameStatus.SECOND_QUARTER
        elif self.status == GameStatus.HALF_TIME:
            self.status = GameStatus.THIRD_QUARTER
        elif self.status == GameStatus.THREE_QUARTER_TIME:
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
            self.score.set_status(GameStatus.FULL_TIME)
            self.log_result()

    def play(self):
        while not self.timer.is_end_of_quarter():
            self.timer.tick()
            self.log_tick()

            field_status, ball_direction, lateral_direction = self.game_matrix.next_state(
                self.field.field_status,
                self.field.position,
                self.ball_direction
            )

            self.field.field_status = field_status
            self.ball_direction = ball_direction

            if ball_direction == BallDirection.FORWARD:
                self.field.move_forward()
            elif ball_direction == BallDirection.BACKWARD:
                self.field.move_backward()
            elif ball_direction == BallDirection.LATERAL and (lateral_direction != LateralDirection.NONE):
                self.field.move_laterally(lateral_direction)

            if self.field.ball_status == BallStatus.GOAL:
                self.score_goal()
            elif self.field.ball_status == BallStatus.BEHIND:
                self.score_behind()

    def log_tick(self):
        possession = self.field.field_status.possession
        ball_status = self.field.field_status.ball_status
        zone = self.field.field_zone
        direction = self.ball_direction
        self.logger.log_message(self.timer, "{}, {}, {}, {}".format(possession, ball_status, zone, direction))

    def score_goal(self):
        team = self.team_in_attack
        self.score.score_goal(team.name)
        self.logger.log_message(self.timer, "{}: GOAL!".format(team.name))
        self.logger.log_short_score(self.timer, self.score)
        self.field.centre_ball()
        self.ball_direction = BallDirection.NONE

    def score_behind(self):
        team = self.team_in_attack
        self.score.score_behind(team.name)
        self.logger.log_message(self.timer, "{}: Behind".format(team.name))
        self.field.switch_possession(BallStatus.FREE_KICK)
        self.ball_direction = BallDirection.FORWARD

    def log_result(self):
        final_score = self.score.get_final_score()
        team_scores = [(team, score.total()) for team, score in final_score.items()]
        margin = abs(team_scores[0][1] - team_scores[1][1])
        
        if margin > 0:
            winning_team = team_scores[0][0] if team_scores[0][1] > team_scores[1][1] else team_scores[1][0]
            result = "{} WON by {} points".format(winning_team, margin)
            self.logger.log_result(result)
        else:
            self.logger.log_result("DRAW")
    
