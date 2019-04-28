import copy
import math

class Move:
    def __init__(self, board, target, source=None):
        self.board = board
        self.target = (
            target[0] % board.num_rings,
            target[1] % board.ring_size)
        if source:
            self.source = (
                source[0] % board.num_rings,
                source[1] % board.ring_size)
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
        if not self.is_valid():
            return False
        if self._creates_spoke_mill():
            return True
        if self._creates_ring_mill():
            return True

        return False

    def _creates_spoke_mill(self):
        #If the move is on a spoke, look for a mill along it.

        spoke_offset = self.board.spoke_period - 1
        target_spoke_offset = self.target[1] % self.board.spoke_period
        if (not self.source or self.target[1] != self.source[1]) and \
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
        break_interval = max(self.board.spoke_period, 2)

        # If target[1] is on a corner, then start != mid != end
        # Otherwise duplicate some work.
        start = (self.target[1] - 1) % self.board.ring_size
        start = (start // break_interval) * break_interval
        mid = (self.target[1] // break_interval) * break_interval
        end = float(self.target[1] + 1) / break_interval
        end = int(math.ceil(end) * break_interval) % self.board.ring_size

        if self._search_for_half_ring_mill(start, mid):
            return True
        if self._search_for_half_ring_mill(mid, end):
            return True

        return False

    def _search_for_half_ring_mill(self, from_index, to_index):
        ring = self.board.rings[self.target[0]]
        index = from_index

        if from_index == to_index:
            return False

        while True:
            if index != self.target[1] and ring[index] != self.board.turn:
                break
            if index == to_index:
                return True
            index = (index + 1) % self.board.ring_size
        
        return False

    @staticmethod
    def get_valid_moves(board):
        phase_calls = {
            board.Phase.place : Move._get_valid_placements
        }

        if board.phase in phase_calls:
            return phase_calls[board.phase](board)

        return None

    @staticmethod
    def _get_valid_placements(board):
        valid_moves = []
        for rings_index in range(board.num_rings):
            for index in range(board.ring_size):
                if board.Player.none is board.rings[rings_index][index]:
                    valid_moves.append(
                        Move(board, (rings_index, index)))
        return valid_moves

    def get_result(self):
        phase_calls = {
            self.board.Phase.place : self._get_placement_result
        }

        if self.is_valid() and self.board.phase in phase_calls:
            return phase_calls[self.board.phase]()

        return None

    def _get_placement_result(self):
        assert self.board.Phase.place is self.board.phase

        new_board = copy.deepcopy(self.board)
        new_board.rings[self.target[0]][self.target[1]] = \
            new_board.turn
        new_board.turn_num += 1

        #TODO resolve a mill.
        if self.creates_mill():
            raise NotImplementedError()

        if new_board.turn_num > (new_board.piece_count * 2):
            new_board.phase = new_board.Phase.move
        self._swtich_player(new_board)
        return new_board

    @staticmethod
    def _swtich_player(board):
        if board.Player.white == board.turn:
            board.turn = board.Player.black
        else:
            board.turn = board.Player.white
