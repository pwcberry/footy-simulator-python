import argparse
import afl
from .football import Football

arg_parser = argparse.ArgumentParser(prog="afl", description="Australian Rules Football game simulator", epilog="Have fun, and I hope your favourite team wins!")
arg_parser.add_argument("-v", "--version", action="version", version="%(prog)s version {0}".format(afl.__version__))
subparsers = arg_parser.add_subparsers(dest="command", title="Simulator commands", metavar="game, season")

parser_season = subparsers.add_parser("game", help="Play a game between two teams")
parser_season.add_argument("-t", "--teams", metavar="teams.yml", action="store", nargs="?", help="The path to the file that defines the teams and their skills")
parser_season.add_argument("home_team", metavar='"Home Team"', action="store", help="The name or abbreviation of the home team")
parser_season.add_argument("away_team", metavar='"Away Team"', action="store", help="The name or abbreviation of the away team")

parser_season = subparsers.add_parser("season", help="Play the home-and-away games of a season")
parser_season.add_argument("-s", "--season", metavar="season.yml", action="store", default="season.yml", help="The path to the file that defines the season, or the season and the teams")
parser_season.add_argument("-t", "--teams", metavar="teams.yml", action="store", nargs="?", default="teams.yml", help="The path to the file that defines the teams and their skills")
parser_season.add_argument("-r", "--rounds", action="store", type=int, nargs="?", help="The number of home-and-away rounds to play for this season")
parser_season.add_argument("-l", "--ladder", action="store_true", help="Display the ladder at the end of the season.")
parser_season.add_argument("-f", "--finals", action="store_true", help="Play finals after the home-and-away season")

args = arg_parser.parse_args()

def main():
    print(vars(args))
    f = Football(args.command, **vars(args))
    print(f)

if __name__ == "__main__":
    main()
