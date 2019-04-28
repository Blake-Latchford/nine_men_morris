#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import copy
from enum import Enum
import logging
import sys

import move

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
        for new_board in board_list[board_index].get_child_boards():
            universal_id = new_board.get_universal_id()
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

    def __init__(self):
        self.rings = list()

        for _ in range(self.num_rings):
            self.rings.append([Board.Player.none] * Board.ring_size)

        self.next_player = Board.Player.white
        self.turn_num = 0

    def is_placing(self):
        return self.turn_num >= 0

    def get_child_boards(self):
        valid_moves = move.Move.get_valid_moves(self)
        child_boards = [x.get_result() for x in valid_moves]
        return self.deduplicate_boards(child_boards)

    @staticmethod
    def deduplicate_boards(boards):
        unique_boards = OrderedDict()
        for board in boards:
            universal_id = board.get_universal_id()
            if universal_id not in unique_boards:
                unique_boards[universal_id] = board

        return list(unique_boards.values())

    def get_universal_id(self):
        ids = set()
        ids.add(self.get_unique_id())
        for board in self.get_equivalent_boards():
            ids.add(board.get_unique_id())
        return sorted(ids)[0]

    def get_unique_id(self):

        # A unique ID is a perfect hash,
        # but isn't guaranteed to fit in Py_ssize_t

        unique_id = self.turn_num + 1
        unique_id = self._combine(unique_id, self.next_player)
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
        ret = 'Turn Number:' + str(self.turn_num) + '\n'
        ret += 'Next Player:' + self.next_player.name + '\n'
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

    def get_winner(self):
        return self.Player.none

if __name__ == '__main__':
    main()
