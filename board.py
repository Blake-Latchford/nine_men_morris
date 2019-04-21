#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import copy
from enum import Enum
import logging
import sys

def main():
    logging.basicConfig(
        filename=sys.argv[0] + ".txt",
        format='%(levelname)s:%(message)s',
        level=logging.DEBUG,
        filemode='w')

    processed_board_ids = set()
    board_list = [Board()]
    board_index = 0

    while board_index < len(board_list):
        #logging.debug(board_list[board_index])
        for new_board in board_list[board_index].get_valid_turns():
            universal_id = new_board.getUniversalID()
            if universal_id not in processed_board_ids:
                processed_board_ids.add(universal_id)
                board_list.append(new_board)
        board_index += 1
    for remaining_board in board_list[board_index:]:
        logging.debug(remaining_board)
    logging.debug(len(board_list))
    logging.debug(board_index)


class Board:

    ring_size = 8
    num_rings = 3
    piece_count = 9
    spoke_period = 2

    Player = Enum('Player', 'none white black')
    Phase = Enum('Phase', 'place move flying')

    def __init__(self):
        self.rings = list()

        for _ in range(self.num_rings):
            self.rings.append([Board.Player.none] * Board.ring_size)

        self.phase = Board.Phase.place
        self.turn = Board.Player.white

    def get_valid_turns(self):
        valid_turns = []
        if self.phase is Board.Phase.place:
            valid_turns = self.get_valid_placements()
        return self.deduplicate_boards(valid_turns)

    @staticmethod
    def deduplicate_boards(boards):
        unique_boards = OrderedDict()
        for board in boards:
            universal_id = board.getUniversalID()
            if universal_id not in unique_boards:
                unique_boards[universal_id] = board

        return list(unique_boards.values())

    def get_valid_placements(self):
        valid_placements = []
        for rings_index in range(len(self.rings)):
            for index in range(Board.ring_size):
                if Board.Player.none is self.rings[rings_index][index]:
                    valid_placements.append(copy.deepcopy(self))
                    valid_placements[-1].rings[rings_index][index] = \
                        self.turn
                    valid_placements[-1]._complete_placement()
        return valid_placements

    def _complete_placement(self):
        for player in (self.Player.black, Board.Player.white):
            if self.count_pieces(player) < Board.piece_count:
                break
        else:
            self.phase = Board.Phase.move
        self._complete_turn()

    def count_pieces(self, player):
        count = 0
        for ring in self.rings:
            for place in ring:
                if place == player:
                    count += 1
        return count

    def _complete_turn(self):
        if Board.Player.white == self.turn:
            self.turn = Board.Player.black
        else:
            self.turn = Board.Player.white

    def get_universal_id(self):
        ids = set()
        ids.add(self.get_unique_id())
        for board in self.get_equivalent_boards():
            ids.add(board.get_unique_id())
        return sorted(ids)[0]

    def get_unique_id(self):

        # A unique ID is a perfect hash,
        # but isn't guaranteed to fit in Py_ssize_t

        unique_id = 0
        unique_id = self._combine(unique_id, self.phase)
        unique_id = self._combine(unique_id, self.turn)
        for ring in self.rings:
            for place in ring:
                unique_id = self._combine(unique_id, place)

        return unique_id

    @staticmethod
    def _combine(original, enum_value):
        return original * len(type(enum_value)) + enum_value.value - 1

    def get_equivalent_boards(self):
        equivalent_boards = list()

        for offset in range(self.spoke_period, self.ring_size,
                            self.spoke_period):
            equivalent_boards.append(
                self.get_rotated(offset))

        for offset in range(self.ring_size // 2):
            equivalent_boards.append(
                self.get_mirrored(offset))

        return equivalent_boards

    def get_rotated(self, offset):
        #Modulo doesn't play nice here.
        offset = offset % self.ring_size

        rotated_board = copy.deepcopy(self)
        for (index, ring) in enumerate(rotated_board.rings):
            rotated_board.rings[index] = ring[-offset:] \
                + ring[:-offset]
        return rotated_board

    def get_mirrored(self, axis):
        mirrored_board = copy.deepcopy(self)

        axis = axis % self.ring_size

        for rings_index in range(self.num_rings):
            for offset in range(self.ring_size // 2):
                positive_offset = (axis + offset) % self.ring_size
                negative_offset = (axis - offset) % self.ring_size
                mirrored_board.rings[rings_index][positive_offset] = \
                    self.rings[rings_index][negative_offset]
                mirrored_board.rings[rings_index][negative_offset] = \
                    self.rings[rings_index][positive_offset]

        return mirrored_board

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        ret = 'Phase:' + self.phase.name + '\n'
        ret += 'Turn:' + self.turn.name + '\n'
        ret += self._board_as_string()
        return ret

    def _board_as_string(self):
        ret = ''
        if self.ring_size != 8:
            return 'Board drawing not implemented.'

        # the upper section

        for (ring_index, ring) in enumerate(self.rings):
            ret += ' ' * ring_index
            gap = ' ' * (self.num_rings - ring_index - 1)
            for place in ring[:self.ring_size // 2 - 1]:
                ret += self._place_to_string(place) + gap
            ret += '\n'

        # center row

        for ring in self.rings:
            ret += self._place_to_string(ring[-1])
        ret += ' '
        for ring in self.rings[::-1]:
            ret += self._place_to_string(ring[self.ring_size // 2 - 1])
        ret += '\n'

        # bottom row

        for (reverse_index, ring) in enumerate(self.rings[::-1]):
            ret += ' ' * (self.num_rings - reverse_index - 1)
            gap = ' ' * reverse_index
            bottom_row = ring[self.ring_size // 2:-1]
            bottom_row.reverse()
            for place in bottom_row:
                ret += self._place_to_string(place) + gap
            ret += '\n'

        return ret

    @staticmethod
    def _place_to_string(place):
        if place is Board.Player.white:
            return 'W'
        elif place is Board.Player.black:
            return 'B'
        else:
            return '.'


if __name__ == '__main__':
    main()
