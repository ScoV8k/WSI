# from Pick import Pick, PickMove, PickState
from games.two_player_games.player import Player
from games.two_player_games.games.Pick import Pick, PickMove, PickState

import math
import random
import itertools


def play(d1, d2, one_player):
    p1 = Player('1')
    p2 = Player('2')
    game = Pick(p1, p2)
    while not game.is_finished():
        state = game.state
        if one_player:
            a_points, a_move = minimax(state, d1, -math.inf, math.inf, True)
            game.make_move(a_move)
            print(f"Wartość ruchu gracza 1: {a_points} \n")
            print(str(game))
            b_move = PickMove(int(input("Wybierz liczbę: ")))
            game.make_move(b_move)
            print(str(game))

        else:
            a_points, a_move = minimax(state, d1, -math.inf, math.inf, True)
            game.make_move(a_move)
            print(f"Wartość ruchu gracza 1: {a_points} \n")
            print(str(game))
            state = game.state
            b_points, b_move = minimax(state, d2, -math.inf, math.inf, False)
            if game.is_finished():
                break
            game.make_move(b_move)
            print(f"Wartość ruchu gracza 2: {b_points} \n")
            print(str(game))


    winner = game.get_winner()
    if winner == p1:
        print("\nWygrywa gracz 1!")
        return 'p1'
    elif winner == p2:
        print("\nWygrywa gracz 2!")
        return 'p2'
    else:
        print("\nRemis!")
        return 'r'


############################################################
############################################################
############################################################

def evaluate(state, max):
    return state.get_heuristic(max)


def minimax(state, depth, alpha, beta, max_player):
    if depth == 0  or state.is_finished():
        if state.is_finished():
            winner = state.get_winner()
            if max_player:
                if winner is state.get_current_player():
                    return 10000, None
                elif winner is not (state.get_current_player() or None):
                    return -10000, None
                else:
                    return 0, None
            else:
                if winner is state.get_current_player():
                    return -10000, None
                elif winner is not (state.get_current_player() or None):
                    return 10000, None
                else:
                    return 0, None
        else:
            return evaluate(state, max_player), None
    if max_player:
        max_evaluation = -math.inf
        possible_moves = state.get_moves()
        random.shuffle(possible_moves)
        best_move = random.choice(possible_moves)
        for move in possible_moves:
            next_state = state.make_move(move)
            evaluation = minimax(next_state, depth - 1, alpha, beta, False)[0]
            if evaluation > max_evaluation:
                max_evaluation = evaluation
                best_move = move
            elif evaluation == max_evaluation:
                best_move = random.choice([best_move, move])
            alpha = max(alpha, max_evaluation)
            if alpha >= beta:
                break
        return max_evaluation, best_move
    else:
        min_evaluation = math.inf
        possible_moves = state.get_moves()
        random.shuffle(possible_moves)
        best_move = random.choice(possible_moves)
        for move in possible_moves:
            next_state = state.make_move(move)
            evaluation = minimax(next_state, depth - 1, alpha, beta, True)[0]
            if evaluation < min_evaluation:
                min_evaluation = evaluation
                best_move = move
            elif evaluation == min_evaluation:
                best_move = random.choice([best_move, move])
            beta = min(beta, min_evaluation)
            if alpha >= beta:
                break
        return min_evaluation, best_move




play(2, 5, False)

