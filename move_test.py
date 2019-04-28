import unittest

from board import Board
from move import Move

class TestMove(unittest.TestCase):
    def test_happy_path(self):
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

    def test_place_on_top(self):
        board = Board()
        board.rings[0][0] = Board.Player.white

        self.assertFalse(
            Move(board, (0, 0)).is_valid())

    def test_place_with_source(self):
        board = Board()
        board = Move(board, (0, 0)).get_result()
        board = Move(board, (0, 1)).get_result()

        self.assertFalse(
            Move(board, (0, 0), (1, 1)).is_valid())

    def test_mill_target(self):
        board = Board()
        board = Move(board, (0, 0)).get_result()
        board = Move(board, (0, 3)).get_result()
        board = Move(board, (0, 1)).get_result()
        board = Move(board, (0, 4)).get_result()

        move = Move(board, (0, 2))

        self.assertFalse(move.is_valid())
        self.assertTrue(move.creates_mill())

        move = Move(board, (0, 2),
                    mill_target=(0, 3))

        self.assertTrue(move.is_valid())
        self.assertTrue(move.creates_mill())

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
        board.rings[0][6] = Board.Player.white

        self.assertFalse(
            Move(board, (0, 0)).creates_mill())
        self.assertFalse(
            Move(board, (0, 7)).creates_mill())

        board.rings[0][7] = Board.Player.white

        self.assertTrue(
            Move(board, (0, 0)).creates_mill())
        self.assertFalse(
            Move(board, (1, 0)).creates_mill())


if __name__ == '__main__':
    unittest.main(exit=False)
