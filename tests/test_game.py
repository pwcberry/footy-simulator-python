import unittest
from unittest.mock import MagicMock, patch
from .context import Game, data as d, status as s

class TestGame(unittest.TestCase):
    def setUp(self):
        self.home_team = d.Team(
            name = "AAA",
            forwards = d.Skills(0.5, 0.5, 0.5),
            mid_field = d.Skills(0.5, 0.5, 0.5),
            backs = d.Skills(0.5, 0.5, 0.5),
            ruck = d.Skills(0.5, 0.5, 0.5)
        )

        self.away_team = d.Team(
            name = "BBB",
            forwards = d.Skills(0.5, 0.5, 0.5),
            mid_field = d.Skills(0.5, 0.5, 0.5),
            backs = d.Skills(0.5, 0.5, 0.5),
            ruck = d.Skills(0.5, 0.5, 0.5)
        )

    @unittest.skip("Need better mocking of 'run' method")
    def test_team_in_attack_home_team(self):
        with patch("afl.game_matrix.GameMatrix") as mock:
            matrix = mock.return_value
            matrix.next_state.return_value = (s.HOME_TEAM_MOVING_STATUS, s.BallDirection.FORWARD, s.LateralDirection.NONE)
            game = Game(self.home_team, self.away_team)
            self.assertEqual(game.team_in_attack, self.home_team)

    @unittest.skip("Need better mocking of 'run' method")
    def test_team_in_attack_away_team(self):
        with patch("afl.field.Field") as mock:
            field = mock.return_value
            print(field)
            game = Game(self.home_team, self.away_team)
            field.possession = s.Possession.AWAY_TEAM
            print(game.field.possession)
            self.assertEqual(game.team_in_attack, self.away_team)

    def test_play_quarter_first_quarter(self):
        output = MagicMock(name="LogOutput")
        game = Game(self.home_team, self.away_team, output)
        game.play = MagicMock(name="game.play")

        game.play_quarter()

        self.assertEqual(game.status, s.GameStatus.QUARTER_TIME)
        game.play.assert_called_once()
        output.write.assert_called()

    def test_play_quarter_second_quarter(self):
        output = MagicMock(name="LogOutput")
        game = Game(self.home_team, self.away_team, output)
        game.play = MagicMock(name="game.play")

        game.play_quarter()
        game.play_quarter()

        self.assertEqual(game.status, s.GameStatus.HALF_TIME)
        self.assertEqual(game.play.call_count, 2)

    def test_play_quarter_third_quarter(self):
        output = MagicMock(name="LogOutput")
        game = Game(self.home_team, self.away_team, output)
        game.play = MagicMock(name="game.play")

        game.play_quarter()
        game.play_quarter()
        game.play_quarter()

        self.assertEqual(game.status, s.GameStatus.THREE_QUARTER_TIME)
        self.assertEqual(game.play.call_count, 3)

    def test_play_quarter_fourth_quarter(self):
        output = MagicMock(name="LogOutput")
        game = Game(self.home_team, self.away_team, output)
        game.play = MagicMock(name="game.play")

        game.play_quarter()
        game.play_quarter()
        game.play_quarter()
        game.play_quarter()

        self.assertEqual(game.status, s.GameStatus.FULL_TIME)
        self.assertEqual(game.play.call_count, 4)
