from games.two_player_games.player import Player
from games.two_player_games.games.Pick import Pick, PickMove, PickState

import math
import random
import itertools

def test_heuristic1():
    ab = Pick(Player('1'), Player('2'))
    ab.make_move(PickMove(7))
    ab.make_move(PickMove(1))
    ab.make_move(PickMove(8))
    ab.make_move(PickMove(2))
    ab.make_move(PickMove(5))
    ab.make_move(PickMove(9))
    ab.make_move(PickMove(14))
    ab.make_move(PickMove(10))
    assert ab.state.get_current_player_numbers() == [7, 8, 5, 14]
    assert ab.state.get_other_player_numbers() == [1, 2, 9, 10]

    assert ab.state.get_heuristic(True) == 954


def test_heuristic2():
    ab = Pick(Player('1'), Player('2'))
    ab.make_move(PickMove(7))
    ab.make_move(PickMove(1))
    ab.make_move(PickMove(8))
    ab.make_move(PickMove(2))
    ab.make_move(PickMove(5))
    ab.make_move(PickMove(9))
    ab.make_move(PickMove(14))
    assert ab.state.get_current_player_numbers() == [1, 2, 9]
    assert ab.state.get_other_player_numbers() == [7, 8, 5, 14]

    assert ab.state.get_heuristic(False) == 14

def test_heuristic3():
    ab = Pick(Player('1'), Player('2'))
    ab.make_move(PickMove(1)) #1
    ab.make_move(PickMove(7)) #2
    ab.make_move(PickMove(2)) #1
    ab.make_move(PickMove(8)) #2
    ab.make_move(PickMove(9)) #1
    ab.make_move(PickMove(5)) #2
    ab.make_move(PickMove(14)) #1
    assert ab.state.get_current_player_numbers() == [7, 8, 5]
    assert ab.state.get_other_player_numbers() == [1, 2, 9, 14]

    assert ab.state.get_heuristic(False) == -3