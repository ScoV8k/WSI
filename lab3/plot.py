from games.two_player_games.player import Player
from games.two_player_games.games.Pick import Pick, PickMove, PickState

from matplotlib import pyplot as plt
import minimax

def make_plot(iterations, d1, d2):
    p1 = 0
    p2 = 0
    r = 0
    for i in range(iterations):
        result = minimax.play(d1, d2, False)
        if result == 'p1':
            p1 += 1
        elif result == 'p2':
            p2 += 1
        elif result == 'r':
            r += 1
    plt.pie([p1, p2, r], autopct='%1.1f%%')
    plt.legend(['Player 1', 'Player 2', 'draw'])
    plt.title(f'Player 1 depth: {d1}, Player 2 depth: {d2}')
    plt.show()

make_plot(50, 4, 4)
