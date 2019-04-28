import copy
import math
from collections import namedtuple

class Move:
    MoveCoordinates = namedtuple(
        "MoveCoordinates",
        ("ring_index", "ring_position"))

    def __init__(self, board, target, source=None):
        self.board = board
        self.target = self._make_move_coordinates(target)
        self.source = self._make_move_coordinates(source)

    def _make_move_coordinates(self, pair):
        if pair is None:
            return None

        return Move.MoveCoordinates(
            int(pair[0]) % self.board.num_rings,
            int(pair[1]) % self.board.ring_size)

    def is_valid(self):
        if self.board.phase is self.board.Phase.place:
            return self._is_valid_placement()

        return False

    def _is_valid_placement(self):
        assert self.board.phase is self.board.Phase.place

        if self.source is not None:
            return False

        target_piece = self.board.rings\
            [self.target.ring_index]\
            [self.target.ring_position]
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

        if (self.source and
                self.target.ring_position == self.source.ring_position):
            return False

        spoke_offset = self.board.spoke_period - 1
        target_spoke_offset = \
            self.target.ring_position % self.board.spoke_period

        if target_spoke_offset != spoke_offset:
            return False

        for rings_index, ring in enumerate(self.board.rings):
            if rings_index == self.target.ring_index:
                continue
            elif ring[self.target.ring_position] != self.board.turn:
                break
        else:
            return True

        return False

    def _creates_ring_mill(self):
        break_interval = max(self.board.spoke_period, 2)

        # If target.ring_position is on a corner, then start != mid != end
        # Otherwise duplicate some work.
        start = (self.target.ring_position - 1) % self.board.ring_size
        start = (start // break_interval) * break_interval
        mid = (self.target.ring_position // break_interval) * break_interval
        end = float(self.target.ring_position + 1) / break_interval
        end = int(math.ceil(end) * break_interval) % self.board.ring_size

        if self._search_for_half_ring_mill(start, mid):
            return True
        if self._search_for_half_ring_mill(mid, end):
            return True

        return False

    def _search_for_half_ring_mill(self, from_index, to_index):
        ring = self.board.rings[self.target.ring_index]
        index = from_index

        if from_index == to_index:
            return False

        while True:
            if (index != self.target.ring_position and
                    ring[index] != self.board.turn):
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
        new_board.rings[self.target.ring_index][self.target.ring_position] = \
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
