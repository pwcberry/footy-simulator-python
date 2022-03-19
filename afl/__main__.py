import argparse
import afl
from .football import Football

arg_parser = argparse.ArgumentParser(prog="afl", usage="%(prog)s [options] [command]", description="Australian Rules Football game simulator", epilog="Have fun, and I hope your favourite team wins!")
arg_parser.add_argument("-v", "--version", action="version", version="%(prog)s version {0}".format(afl.__version__))
arg_parser.add_argument("--log-level", action="store", nargs="?", choices=["FINAL", "QUARTER", "SCORE", "GOAL", "ACTION"], default="ACTION", help="determine the level for logging")
subparsers = arg_parser.add_subparsers(dest="command", title="Simulator commands", metavar="game, season")

parser_season = subparsers.add_parser("game", prog="afl", usage='%(prog)s [options] game "Home Team" "Away Team"', help="Play a game between two teams")
parser_season.add_argument("-t", "--teams", metavar="teams.yml", action="store", nargs="?", help="the path to the file that defines the teams and their skills")
parser_season.add_argument("home_team", metavar='"Home Team"', action="store", help="the name or abbreviation of the home team")
parser_season.add_argument("away_team", metavar='"Away Team"', action="store", help="the name or abbreviation of the away team")

parser_season = subparsers.add_parser("season", prog="afl", usage='%(prog)s [options] season', help="Play the home-and-away games of a season")
parser_season.add_argument("-s", "--season", metavar="season.yml", action="store", default="season.yml", help="the path to the file that defines the season, or the season and the teams")
parser_season.add_argument("-t", "--teams", metavar="teams.yml", action="store", nargs="?", default="teams.yml", help="the path to the file that defines the teams and their skills")
parser_season.add_argument("-r", "--rounds", action="store", type=int, default=22, nargs="?", help="the number of home-and-away rounds to play for this season. Default: %(default)s")
parser_season.add_argument("-l", "--ladder", action="store_true", help="display the ladder at the end of the season.")
parser_season.add_argument("-f", "--finals", action="store_true", help="play finals after the home-and-away season")

args = arg_parser.parse_args()

def main():
    if args.command == None:
        print('You must specify a command to play a "game" or a "season"\n')        
        arg_parser.print_help()
        exit()

    f = Football(args.command, **vars(args))
    print(f)

if __name__ == "__main__":
    main()
