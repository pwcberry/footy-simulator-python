import unittest
from unittest.mock import MagicMock, patch

import afl
from .context import Game, data as d, status as s
from .fixture import MockBuffer

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

    def test_run_sets_team_in_attack_home_team(self):
        output = MagicMock(name="LogOutput")
        with patch.object(afl.timer.Timer, "is_end_of_quarter") as timer_mock:
            timer_mock.side_effect = [False, True]

            with patch.object(afl.game_matrix.GameMatrix, "next_state") as matrix_mock:
                matrix_mock.return_value = (s.HOME_TEAM_MOVING_STATUS, s.BallDirection.FORWARD, s.LateralDirection.NONE)
                game = Game(self.home_team, self.away_team, output)
                game.play()
                self.assertEqual(game.team_in_attack, self.home_team)
                matrix_mock.reset_mock()
            
            timer_mock.reset_mock()

    def test_run_setsteam_in_attack_away_team(self):
        output = MagicMock(name="LogOutput")
        with patch.object(afl.timer.Timer, "is_end_of_quarter") as timer_mock:
            timer_mock.side_effect = [False, True]

            with patch.object(afl.game_matrix.GameMatrix, "next_state") as matrix_mock:
                matrix_mock.return_value = (s.AWAY_TEAM_MOVING_STATUS, s.BallDirection.FORWARD, s.LateralDirection.NONE)
                game = Game(self.home_team, self.away_team, output)
                game.play()
                self.assertEqual(game.team_in_attack, self.away_team)
                matrix_mock.reset_mock()
            
            timer_mock.reset_mock()

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
