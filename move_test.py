import unittest

from board import Board
from move import Move

class TestPlacement(unittest.TestCase):
    def test_happy_path(self):
        board = Board()

        self.assertTrue(
            Move(board, (0, 0)).is_valid())
        self.assertTrue(
            Move(board, ("0", "0")).is_valid())
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

    def test_move_properties(self):
        board = Board()
        move = Move(board, (0, 0))
        move.source = (1, 1)
        move.mill_target = (2, 2)

        self.assertIsInstance(move.target, move.MoveCoordinates)
        self.assertIsInstance(move.source, move.MoveCoordinates)
        self.assertIsInstance(move.mill_target, move.MoveCoordinates)

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

        board = move.get_result()

        self.assertIs(board.rings[0][2], board.Player.white)
        self.assertIs(board.rings[0][3], board.Player.none)

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

class TestMoving(unittest.TestCase):
    def setUp(self):
        board = Board()
        self.board = board

        board.turn_num = -1
        board.rings[0][1] = board.Player.white
        board.rings[0][2] = board.Player.white
        board.rings[0][7] = board.Player.white
        board.rings[1][1] = board.Player.white
        board.rings[2][2] = board.Player.white

        board.rings[1][4] = board.Player.black
        board.rings[2][5] = board.Player.black
        board.rings[1][6] = board.Player.black
        board.rings[2][0] = board.Player.black

    def test_valid_white_shifts(self):
        instructuions = (
            # Make ring mill accross wrap boundary
            ((0, 7), (0, 0), (1, 4), True),
            # Make spoke mill
            ((2, 2), (2, 1), (1, 4), True),
            ((0, 1), (0, 0), None, False),
            ((0, 7), (0, 6), None, False),
        )

        self.board.next_player = self.board.Player.white

        for instruction in instructuions:
            with self.subTest(instruction=instruction):
                source, target, mill_target, result = instruction
                move = Move(self.board, target, source, mill_target)
                self.assertTrue(move.is_valid())
                self.assertEqual(move.creates_mill(), result)

    def test_valid_black_shifts(self):
        instructuions = (
            # ring mill
            ((2, 5), (1, 5), (0, 2), True),
            # block white spoke mill
            ((2, 0), (2, 1), None, False),
        )

        self.board.next_player = self.board.Player.black


        for instruction in instructuions:
            with self.subTest(instruction=instruction):
                source, target, mill_target, result = instruction
                move = Move(self.board, target, source, mill_target)
                self.assertTrue(move.is_valid())
                self.assertEqual(move.creates_mill(), result)

    def test_invalid_shifts(self):
        instructuions = (
            # diagonal shift
            ((0, 2), (1, 2)),
            # shift on top
            ((0, 1), (0, 2)),
            # source is none
            ((0, 5), (0, 6)),
            # source is none
            ((1, 4), (1, 5)),
        )

        self.board.next_player = self.board.Player.white

        for instruction in instructuions:
            with self.subTest(instruction=instruction):
                source, target = instruction
                move = Move(self.board, target, source)
                self.assertFalse(move.is_valid())

if __name__ == '__main__':
    unittest.main(exit=False)
