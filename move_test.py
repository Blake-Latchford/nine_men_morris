import unittest

from board import Board
from move import Move

class TestIsValid(unittest.TestCase):
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

class TestMills(unittest.TestCase):
    def test_creates_mill_invalid_move(self):
        board = Board()
        board.rings[0][0] = Board.Player.white

        self.assertFalse(
            Move(board, (0, 0)).creates_mill())

    def test_creates_spoke_mill(self):
        board = Board()
        board.rings[0][1] = Board.Player.white

        self.assertFalse(
            Move(board, (1, 1)).creates_mill())

        board.rings[2][1] = Board.Player.white

        self.assertTrue(
            Move(board, (1, 1)).creates_mill())
        self.assertFalse(
            Move(board, (0, 0)).creates_mill())

        board.rings[1][1] = Board.Player.white

        self.assertFalse(
            Move(board, (0, 0)).creates_mill())

    def test_creates_ring_mill_upper(self):
        board = Board()
        board.rings[0][1] = Board.Player.white

        self.assertFalse(
            Move(board, (0, 0)).creates_mill())

        board.rings[0][2] = Board.Player.white

        self.assertTrue(
            Move(board, (0, 0)).creates_mill())
        self.assertFalse(
            Move(board, (0, -1)).creates_mill())

        board.rings[0][3] = Board.Player.white

        self.assertTrue(
            Move(board, (0, 4)).creates_mill())
        self.assertFalse(
            Move(board, (0, -1)).creates_mill())

    def test_creates_ring_mill_lower(self):
        board = Board()
        board.rings[0][6] = Board.Player.none
        
        self.assertFalse(
            Move(board, (0, 0)).creates_mill())
        self.assertFalse(
            Move(board, (0, 7)).creates_mill())
        
        board.rings[0][7] = Board.Player.white

        self.assertTrue(
            Move(board, (0, -1)).creates_mill())
        self.assertFalse(
            Move(board, (1, -1)).creates_mill())


if __name__ == '__main__':
    unittest.main(exit=False)
