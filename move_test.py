import unittest

from board import Board
from move import Move

class TestOperations(unittest.TestCase):
    def test_is_valid_happy_path(self):
        board = Board()

        self.assertTrue(
            Move(board, (0, 0)).is_valid())
        self.assertTrue(
            Move(board, (1, 4)).is_valid())
        self.assertTrue(
            Move(board, (2, 7)).is_valid())
        self.assertTrue(
            Move(board, (-1, 0)).is_valid())
        self.assertTrue(
            Move(board, (0, -1)).is_valid())
        self.assertTrue(
            Move(board, (board.num_rings, 0)).is_valid())
        self.assertTrue(
            Move(board, (0, board.ring_size)).is_valid())

    def test_is_valid_place_on_top(self):
        board = Board()
        board.rings[0][0] = Board.Player.white

        self.assertFalse(
            Move(board, (0, 0)).is_valid())

    def test_creates_spoke_mill(self):
        board = Board()
        board.rings[0][1] = Board.Player.white
        board.rings[2][1] = Board.Player.white

        self.assertTrue(
            Move(board, (1, 1)).creates_mill())
        self.assertFalse(
            Move(board, (0, 0)).creates_mill())

        board.rings[1][1] = Board.Player.white

        self.assertFalse(
            Move(board, (1, 1)).creates_mill())
        self.assertFalse(
            Move(board, (0, 0)).creates_mill())

if __name__ == '__main__':
    unittest.main(exit=False)
