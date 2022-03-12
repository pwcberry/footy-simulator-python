import unittest
from unittest.mock import MagicMock, Mock, patch
from status import GameStatus, Possession
from data import Skills, Team
from game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.home_team = Team(
            name = "AAA",
            forwards = Skills(0.5, 0.5, 0.5),
            mid_field = Skills(0.5, 0.5, 0.5),
            backs = Skills(0.5, 0.5, 0.5),
            ruck = Skills(0.5, 0.5, 0.5)
        )

        self.away_team = Team(
            name = "BBB",
            forwards = Skills(0.5, 0.5, 0.5),
            mid_field = Skills(0.5, 0.5, 0.5),
            backs = Skills(0.5, 0.5, 0.5),
            ruck = Skills(0.5, 0.5, 0.5)
        )

    def test_team_in_attack_home_team(self):
        with patch("field.Field") as mock:
            field = mock.return_value
            game = Game(self.home_team, self.away_team)
            field.possession = Possession.HOME_TEAM
            self.assertEqual(game.team_in_attack, self.home_team)

    def test_team_in_attack_away_team(self):
        with patch("field.Field") as mock:
            field = mock.return_value
            game = Game(self.home_team, self.away_team)
            field.possession = Possession.AWAY_TEAM
            self.assertEqual(game.team_in_attack, self.away_team)

    def test_play_quarter_first_quarter(self):
        output = MagicMock(name="LogOutput")
        game = Game(self.home_team, self.away_team, output)
        game.play = MagicMock(name="game.play")

        game.play_quarter()

        self.assertEqual(game.status, GameStatus.QUARTER_TIME)
        game.play.assert_called_once()
        output.write.assert_called()

    def test_play_quarter_second_quarter(self):
        output = MagicMock(name="LogOutput")
        game = Game(self.home_team, self.away_team, output)
        game.play = MagicMock(name="game.play")

        game.play_quarter()
        game.play_quarter()

        self.assertEqual(game.status, GameStatus.HALF_TIME)
        self.assertEqual(game.play.call_count, 2)

    def test_play_quarter_third_quarter(self):
        output = MagicMock(name="LogOutput")
        game = Game(self.home_team, self.away_team, output)
        game.play = MagicMock(name="game.play")

        game.play_quarter()
        game.play_quarter()
        game.play_quarter()

        self.assertEqual(game.status, GameStatus.THREE_QUARTER_TIME)
        self.assertEqual(game.play.call_count, 3)

    def test_play_quarter_fourth_quarter(self):
        output = MagicMock(name="LogOutput")
        game = Game(self.home_team, self.away_team, output)
        game.play = MagicMock(name="game.play")

        game.play_quarter()
        game.play_quarter()
        game.play_quarter()
        game.play_quarter()

        self.assertEqual(game.status, GameStatus.FULL_TIME)
        self.assertEqual(game.play.call_count, 4)



if __name__ == "__main__":
    unittest.main()
