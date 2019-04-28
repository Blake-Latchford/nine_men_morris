import copy
import math
from collections import namedtuple

class Move:
    MoveCoordinates = namedtuple(
        "MoveCoordinates",
        ("ring_index", "ring_position"))

    def __init__(self, board, target, source=None, mill_target=None):
        self.board = board
        self.target = target
        self.source = source
        self.mill_target = mill_target

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = self._make_move_coordinates(value)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = self._make_move_coordinates(value)

    @property
    def mill_target(self):
        return self._mill_target

    @mill_target.setter
    def mill_target(self, value):
        self._mill_target = self._make_move_coordinates(value)

    def _make_move_coordinates(self, pair):
        if pair is None:
            return None

        return Move.MoveCoordinates(
            int(pair[0]) % self.board.num_rings,
            int(pair[1]) % self.board.ring_size)

    def is_valid(self):
        return self._is_valid_move() and self._is_valid_mill()

    def _is_valid_mill(self):
        if not self.creates_mill():
            return True
        if self.mill_target is None:
            return False

        mill_target_player = self.board.rings\
            [self.mill_target.ring_index]\
            [self.mill_target.ring_position]
        expected_mill_target_player = \
            self._other_player(self.board)
        
        return mill_target_player == expected_mill_target_player

    def _is_valid_move(self):
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
        if not self._is_valid_move():
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

        if self.creates_mill():
            new_board.rings \
                [self.mill_target.ring_index] \
                [self.mill_target.ring_position] = self.board.Player.none

        if new_board.turn_num > (new_board.piece_count * 2):
            new_board.phase = new_board.Phase.move
        new_board.turn = self._other_player(self.board)
        return new_board

    @staticmethod
    def _other_player(board):
        if board.Player.white == board.turn:
            return board.Player.black
        else:
            return board.Player.white
