import unittest
from board import Board

class TestOperations(unittest.TestCase):
    def test_rotate(self):
        for rings_index in range(Board.num_rings):
            original = Board()
            original.rings[rings_index][0] = Board.Player.white

            for offset in range(Board.ring_size):
                rotated = Board()
                rotated.rings[rings_index][offset] = Board.Player.white

                with self.subTest(offset=offset):
                    self.assertEqual(original.get_rotated(offset), rotated)

    def test_mirror(self):
        test_cases = (
            (0, 0, 0),
            (0, 1, 7),
            (0, 4, 4),
            (1, 1, 1),
            (1, 0, 2),
            (7, 0, 6),
        )

        for rings_index in range(Board.num_rings):
            for offset, start_index, end_index in test_cases:
                with self.subTest(
                    start_index=start_index,
                    end_index=end_index,
                    offset=offset):

                    origianl = Board()
                    mirrored = Board()

                    origianl.rings[rings_index][start_index] = \
                        Board.Player.white
                    mirrored.rings[rings_index][end_index] = \
                        Board.Player.white

                    self.assertEqual(origianl.get_mirrored(offset), mirrored)

class TestIDs(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(
            Board().get_universal_id(),
            Board().get_universal_id())

    def test_different(self):
        origianl = Board()
        for rings_index in range(Board.num_rings):
            for index in range(Board.ring_size):
                modified = Board()

                modified.rings[rings_index][index] = Board.Player.white

                self.assertNotEqual(origianl, modified)
                self.assertNotEqual(
                    origianl.get_universal_id(),
                    modified.get_universal_id())

    def test_equivalent(self):
        for rings_index in range(Board.num_rings):
            for index in range(Board.ring_size):
                original = Board()

                original.rings[rings_index][index] = Board.Player.white

                for equivalent in original.get_equivalent_boards():
                    with self.subTest(
                        original=original,
                        equivalent=equivalent,
                        rings_index=rings_index,
                        index=index):
                        self.assertEqual(
                            original.get_universal_id(),
                            equivalent.get_universal_id())

class TestWinner(unittest.TestCase):
    def setUp(self):
        self.board = Board()

        self.board.rings[0][0] = Board.Player.white
        self.board.rings[0][1] = Board.Player.white
        self.board.rings[0][2] = Board.Player.white

        self.board.rings[1][0] = Board.Player.black
        self.board.rings[1][1] = Board.Player.black
        self.board.rings[1][2] = Board.Player.black

    def test_none(self):
        self.assertIs(self.board.get_winner(),
                      self.board.Player.none)

    def test_white(self):
        self.board.rings[1][2] = Board.Player.none
        self.assertIs(self.board.get_winner(),
                      self.board.Player.white)

    def test_black(self):
        self.board.rings[0][2] = Board.Player.none
        self.assertIs(self.board.get_winner(),
                      self.board.Player.black)

if __name__ == '__main__':
    unittest.main(exit=False)
