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
        try:
            move_strings = sys.stdin.readline().split()

            if len(move_strings) != 2:
                print("Move command in format '<ring_index> <ring_position>")
                continue
            
            move_ints = [int(x) for x in move_strings]

            move = Move(board, move_ints )

            if not move.is_valid():
                print("Invalid move specified")
                move = None
        except ValueError as value_error:
            print(value_error)

    return move



if __name__ == '__main__':
    main()
