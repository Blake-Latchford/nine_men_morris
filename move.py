


class Move:
    def __init__(self, board, target, source=None):
        self.board = board
        self.target = (
            target[0] % board.num_rings,
            target[1] % board.num_rings)
        if source:
            self.source = (
                source[0] % board.num_rings,
                source[1] % board.num_rings)
        else:
            self.source = None

    def is_valid(self):
        if self.board.phase is self.board.Phase.place:
            return self._is_valid_placement()

        return False

    def _is_valid_placement(self):
        assert self.board.phase is self.board.Phase.place

        if self.source is not None:
            return False

        target_piece = self.board.rings[self.target[0]][self.target[1]]
        return target_piece is self.board.Player.none

    def creates_mill(self):
        if self._creates_spoke_mill():
            return True

        return self._creates_ring_mill()

    def _creates_spoke_mill(self):
        #If the move is on a spoke, look for a mill along it.

        spoke_offset = self.board.spoke_period - 1
        target_spoke_offset = self.target[1] % self.board.spoke_period
        if self.target[1] != self.source[1] and \
                target_spoke_offset == spoke_offset:
            for rings_index, ring in enumerate(self.board.rings):
                if rings_index == self.target[0]:
                    continue
                elif ring[self.target[1]] != self.board.turn:
                    break
            else:
                return True

        return False

    def _creates_ring_mill(self):
        if not self.source:
            return False

        ring = self.board.rings[self.target[0]]

        break_interval = max(self.board.spoke_period, 2)

        # If target[1] is on a corner, then start != mid != end
        # Otherwise we'll duplicate some work.
        start = ((self.target[1] - 1) // break_interval) * break_interval
        mid = (self.target[1] // break_interval) * break_interval
        end = ((self.target[1] + 1) // break_interval) * break_interval


        adjacent_count = 1
        for offset in range(1, 3):
            position = self.target[1] + offset
            if ring[position] != self.board.turn:
                break
            if self.source and self.source[0] == self.target[0] and \
                    self.source[1] == position:
                break

        return adjacent_count > 3
