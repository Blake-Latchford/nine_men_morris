from board import board
import copy
import unittest

class TestOperations(unittest.TestCase):
    def test_rotate(self):
        for rings_index in range(board._num_rings):
            a = board()
            a._rings[rings_index][0] = board.Player.white
            
            for offset in range(board._ring_size):
                b = board()
                b._rings[rings_index][offset] = board.Player.white
                
                with self.subTest(offset=offset):
                    self.assertEqual(a.getRotated(offset), b)
    
    def test_mirror(self):
        test_cases = (
            (0, 0, 0),
            (0, 1, 7),
            (0, 4, 4),
            (1, 1, 1),
            (1, 0, 2),
            (7, 0, 6),
        )
        
        for rings_index in range(board._num_rings):
            for offset, start_index, end_index in test_cases:
                with self.subTest(start_index=start_index, end_index=end_index, offset=offset):
                    a = board()
                    b = board()
                    
                    a._rings[rings_index][start_index] = board.Player.white
                    b._rings[rings_index][end_index] = board.Player.white
                    
                    self.assertEqual(a.getMirrored(offset), b)

class TestIDs(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(
            board().getUniversalID(),
            board().getUniversalID())
        
    def test_different(self):
        a = board()
        for rings_index in range(board._num_rings):
            for index in range(board._ring_size):
                b = board()
                
                b._rings[rings_index][index] = board.Player.white
                
                self.assertNotEqual(a, b)
                self.assertNotEqual(
                    a.getUniversalID(),
                    b.getUniversalID())
    
    def test_equivalent(self):
        for rings_index in range(board._num_rings):
            for index in range(board._ring_size):
                a = board()
                
                a._rings[rings_index][index] = board.Player.white
                
                for b in a._getEquivalentBoards():
                    with self.subTest(a=a, b=b, rings_index=rings_index, index=index):
                        self.assertEqual(
                            a.getUniversalID(),
                            b.getUniversalID())
                
if __name__ == '__main__':
    unittest.main(exit=False)