from .data import Skills, Team
from .game import Game

# This is a simulation of an Australian Rules Football game.
#
# Inputs are:
#
# 2 Teams
# Their rating for defence: in preventing scores and moving the ball to the mid-field
# Their rating for mid-field: retaining the ball and moving to the forward line
# Their rating for forwards: ability take possession and score
# Their rating for team cohesion
# Their rating for team (physical) health
# Their rating for goal kicking accuracy
# Ratings are a float between 0 and 1

# The output will be:
# Scores at 1/4 time, half time, 3/4 time and full time.


def play_game(home_team, away_team):
    game = Game(home_team, away_team)

    game.play_quarter()
    game.play_quarter()
    game.play_quarter()
    game.play_quarter()



def define_team(name):
    print("You will be providing a rating on the characteristics of the team:", name)
    print("Each rating is a value between 0 and 1, where 1 is represents the strongest rating")
    print("")
    forwards =  eval(input("Rate the forwards    : "))
    mid_field = eval(input("Rate the mid field   : "))
    defense =   eval(input("Rate the defense     : "))
    cohesion =  eval(input("Rate team cohesion   : "))
    health =    eval(input("Rate team fitness    : "))
    accuracy =  eval(input("Rate accuracy at goal: "))

    return Team(name, forwards, mid_field, defense, cohesion, health, accuracy)


def define_teams():
    print("Enter the team names")
    home_team_name = input("Enter the home team's name: ")
    away_team_name = input("Enter the away team's name: ")

    home_team = define_team(home_team_name)
    away_team = define_team(away_team_name)

    return home_team, away_team


def set_home_team():
    return Team(
        "Essendon",
        forwards = Skills(accuracy = 0, pressure = 0, strength = 0),
        mid_field= Skills(accuracy = 0, pressure = 0, strength = 0),
        backs    = Skills(accuracy = 0, pressure = 0, strength = 0),
        ruck     = Skills(accuracy = 0, pressure = 0, strength = 0),
        cohesion = 0,
        fitness = 1
    )

def set_away_team():
    return Team(
        "Richmond",
        forwards = Skills(accuracy = 0, pressure = 0, strength = 0),
        mid_field= Skills(accuracy = 0, pressure = 0, strength = 0),
        backs    = Skills(accuracy = 0, pressure = 0, strength = 0),
        ruck     = Skills(accuracy = 0, pressure = 0, strength = 0),
        cohesion = 0,
        fitness = 1
    )


def main():
    # home_team, away_team = define_teams()
    home_team, away_team = set_home_team(), set_away_team()
    play_game(home_team, away_team)

class Football:
    def __init__(self, sim_type, **kwargs):
        self.sim_type = sim_type
        self.teams_file = kwargs.get("teams")
        self.season_file = kwargs.get("season")
        self.season_rounds = kwargs.get("rounds") if sim_type == "season" else 0
        self.show_ladder = kwargs.get("ladder") if sim_type == "season" else False
        self.have_finals = kwargs.get("finals") if sim_type == "season" else False

    
