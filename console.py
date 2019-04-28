import sys

from board import Board
from move import Move

def main():
    board = Board()

    while board.get_winner() is Board.Player.none:
        print(board)
        board = get_move(board).get_result()

def get_move(board):
    move = None

    while not move:
        print("Move location:")
        move = Move(board, get_pair())
        if move.creates_mill():
            print("Specify mill target")
            move.mill_target = get_pair()

        if not move.is_valid():
            move = None

    return move

def get_pair():
    pair = None

    while not pair:
        try:
            pair_strings = sys.stdin.readline().split()

            if len(pair_strings) != 2:
                print("Move command in format '<ring_index> <ring_position>'")
                continue

            pair = [int(x) for x in pair_strings]
        except ValueError as value_error:
            pair = None
            print(value_error)
    
    return pair

if __name__ == '__main__':
    main()
