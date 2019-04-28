import copy
import math
from collections import namedtuple

class Move:
    MoveCoordinates = namedtuple(
        "MoveCoordinates",
        ("ring_index", "ring_position"))

    def __init__(self, board, target, source=None, mill_target=None):
        assert board
        self.board = board

        self._target = None
        self._source = None
        self._mill_target = None

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

        mill_target_player = self._get_player(self.mill_target)
        expected_mill_target_player = self._last_player(self.board)

        return mill_target_player == expected_mill_target_player

    def _is_valid_move(self):
        return self._is_valid_placement() or self._is_valid_shift()

    def _is_valid_placement(self):
        if not self.board.is_placing():
            return False

        if self.source is not None:
            return False

        target_player = self._get_player(self.target)
        return target_player is self.board.Player.none

    def _is_valid_shift(self):
        if self.board.is_placing():
            return False

        if self._get_player(self.source) != self.board.next_player:
            return False

        if self._get_player(self.target) != self.board.Player.none:
            return False

        if self.source.ring_index == self.target.ring_index:
            distance = self.source.ring_position - self.target.ring_position
            distance = abs(distance)
            if distance in (1, 7):
                return True
        elif self.source.ring_position == self.target.ring_position:
            spoke_offset = self.board.spoke_period - 1
            target_spoke_offset = \
                self.target.ring_position % self.board.spoke_period
            if spoke_offset == target_spoke_offset:
                return True
        return False

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

        for ring_index, ring in enumerate(self.board.rings):
            if ring_index == self.target.ring_index:
                continue
            elif ring[self.target.ring_position] != self.board.next_player:
                break
        else:
            return True

        return False

    def _creates_ring_mill(self):
        break_interval = max(self.board.spoke_period, 2)

        # If target.ring_position is on a corner, then start != mid != end
        start = (self.target.ring_position - 1) % self.board.ring_size
        start = (start // break_interval) * break_interval
        mid = (self.target.ring_position // break_interval) * break_interval
        end = float(self.target.ring_position + 1) / break_interval
        end = int(math.ceil(end) * break_interval) % self.board.ring_size

        if self._search_for_ring_mill(start, mid):
            return True
        if self._search_for_ring_mill(mid, end):
            return True

        return False

    def _search_for_ring_mill(self, from_index, to_index):
        ring = self.board.rings[self.target.ring_index]
        index = from_index

        if from_index == to_index:
            return False

        while True:
            if (index != self.target.ring_position and
                    ring[index] != self.board.next_player):
                break
            if (self.source is not None and
                    self.source.ring_index == self.target.ring_index and
                    index == self.source.ring_position):
                return False
            if index == to_index:
                return True
            index = (index + 1) % self.board.ring_size

        return False

    @staticmethod
    def get_valid_moves(board):
        if board.is_placing():
            return Move._get_valid_placements(board)

        return None

    @staticmethod
    def _get_valid_placements(board):
        valid_moves = []
        for ring_index in range(board.num_rings):
            for index in range(board.ring_size):
                if board.Player.none is board.rings[ring_index][index]:
                    valid_moves.append(
                        Move(board, (ring_index, index)))
        return valid_moves

    def get_result(self):
        if self.board.is_placing():
            return self._get_placement_result()

        return None

    def _get_placement_result(self):
        assert self.board.is_placing()

        new_board = copy.deepcopy(self.board)
        new_board.rings[self.target.ring_index][self.target.ring_position] = \
            new_board.next_player
        new_board.turn_num += 1

        if self.creates_mill():
            new_board.rings \
                [self.mill_target.ring_index] \
                [self.mill_target.ring_position] = self.board.Player.none

        if new_board.turn_num > (new_board.piece_count * 2):
            new_board.turn_num = -1
        new_board.next_player = self._last_player(self.board)
        return new_board

    @staticmethod
    def _last_player(board):
        if board.Player.white == board.next_player:
            return board.Player.black
        else:
            return board.Player.white

    def _get_player(self, position):
        return self.board.rings[position.ring_index][position.ring_position]

    def __str__(self):
        return (
            "target(" + str(self._target) + ")" +
            "source(" + str(self._source) + ")" +
            "mill_target(" + str(self._mill_target) + ")"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
