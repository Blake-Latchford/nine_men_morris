#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict 
import copy
from enum import Enum
import logging
import os.path
import sys

def main():
    logging.basicConfig(
        filename=sys.argv[0] + ".txt",
        format='%(levelname)s:%(message)s',
        level=logging.DEBUG,
        filemode='w')
        
    processedBoardIDs = set()
    board_list = [board()]
    board_index = 0
    
    while board_index < len(board_list):
        #logging.debug(board_list[board_index])
        for new_board in board_list[board_index].getValidTurns():
            universalID = new_board.getUniversalID()
            if universalID not in processedBoardIDs:
                processedBoardIDs.add(universalID)
                board_list.append(new_board)
        board_index += 1
    for b in board_list[board_index:]:
        logging.debug(b)
    logging.debug(len(board_list))
    logging.debug(board_index)

        
class board:

    _ring_size = 8
    _num_rings = 3
    _piece_count = 9
    _spoke_period = 2

    Player = Enum('Player', 'none white black')
    Phase = Enum('Phase', 'place move flying')

    def __init__(self):
        self._rings = list()

        for _ in range(self._num_rings):
            self._rings.append([board.Player.none] * board._ring_size)

        self.phase = board.Phase.place
        self.turn = board.Player.white

    def getValidTurns(self):
        validTurns = []
        if self.phase is board.Phase.place:
            validTurns = self.getValidPlacements()
        return self.deduplicateBoards(validTurns)

    @staticmethod
    def deduplicateBoards(boards):
        uniqueBoards = OrderedDict()
        for board in boards:
            universalID = board.getUniversalID()
            if universalID not in uniqueBoards:
                uniqueBoards[universalID] = board

        return list(uniqueBoards.values())

    def getValidPlacements(self):
        validPlacements = []
        for rings_index in range(len(self._rings)):
            for index in range(board._ring_size):
                if board.Player.none is self._rings[rings_index][index]:
                    validPlacements.append(copy.deepcopy(self))
                    validPlacements[-1]._rings[rings_index][index] = \
                        self.turn
                    validPlacements[-1].completePlacement()
        return validPlacements

    def completePlacement(self):
        for player in (self.Player.black, board.Player.white):
            if self.countPieces(player) < board._piece_count:
                break
        else:
            self.phase = board.Phase.move
        self.completeTurn()

    def countPieces(self, player):
        count = 0
        for ring in self._rings:
            for place in ring:
                if place == player:
                    count += 1
        return count

    def completeTurn(self):
        if board.Player.white == self.turn:
            self.turn = board.Player.black
        else:
            self.turn = board.Player.white

    def getUniversalID(self):
        ids = set()
        ids.add(self.getUniqueID())
        for board in self._getEquivalentBoards():
            ids.add(board.getUniqueID())
        return sorted(ids)[0]

    def getUniqueID(self):

        # A unique ID is a perfect hash, but isn't guaranteed to fit in Py_ssize_t

        uniqueID = 0
        uniqueID = self._combine(uniqueID, self.phase)
        uniqueID = self._combine(uniqueID, self.turn)
        for ring in self._rings:
            for place in ring:
                uniqueID = self._combine(uniqueID, place)
                
        return uniqueID

    @staticmethod
    def _combine(original, enum_value):
        return original * len(type(enum_value)) + enum_value.value - 1

    def _getEquivalentBoards(self):
        equivalentBoards = list()

        for offset in range(self._spoke_period, self._ring_size,
                            self._spoke_period):
            equivalentBoards.append(
                self.getRotated(offset))
                
        for offset in range(self._ring_size // 2):
            equivalentBoards.append(
                self.getMirrored(offset))

        return equivalentBoards
        
    def getRotated(self, offset):
        #Modulo doesn't play nice here.
        offset = offset % self._ring_size
    
        rotatedBoard = copy.deepcopy(self)
        for (index, ring) in enumerate(rotatedBoard._rings):
            rotatedBoard._rings[index] = ring[-offset:] \
                + ring[:-offset]
        return rotatedBoard

    def getMirrored(self, axis):
        mirroredBoard = copy.deepcopy(self)
        
        axis = axis % self._ring_size
        
        for rings_index in range(self._num_rings):
            for offset in range(self._ring_size // 2):
                positive_offset = (axis + offset) % self._ring_size
                negative_offset = (axis - offset) % self._ring_size
                mirroredBoard._rings[rings_index][positive_offset] = \
                    self._rings[rings_index][negative_offset]
                mirroredBoard._rings[rings_index][negative_offset] = \
                    self._rings[rings_index][positive_offset]
            
        return mirroredBoard
        
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        ret = 'Phase:' + self.phase.name + '\n'
        ret += 'Turn:' + self.turn.name + '\n'
        ret += self._boardAsString()
        return ret

    def _boardAsString(self):
        ret = ''
        if self._ring_size != 8:
            return 'Board drawing not implemented.'

        # the upper section

        for (ring_index, ring) in enumerate(self._rings):
            ret += ' ' * ring_index
            gap = ' ' * (self._num_rings - ring_index - 1)
            for place in ring[:self._ring_size // 2 - 1]:
                ret += self._placeToString(place) + gap
            ret += '\n'

        # center row

        for ring in self._rings:
            ret += self._placeToString(ring[-1])
        ret += ' '
        for ring in self._rings[::-1]:
            ret += self._placeToString(ring[self._ring_size // 2 - 1])
        ret += '\n'

        # bottom row
        
        for (reverse_index, ring) in enumerate(self._rings[::-1]):
            ret += ' ' * (self._num_rings - reverse_index - 1)
            gap = ' ' * reverse_index
            bottom_row = ring[self._ring_size // 2:-1]
            bottom_row.reverse()
            for place in bottom_row:
                ret += self._placeToString(place) + gap
            ret += '\n'

        return ret
        
    @staticmethod
    def _placeToString(place):
        if place is board.Player.white:
            return 'W'
        elif place is board.Player.black:
            return 'B'
        else:
            return '.'


if __name__ == '__main__':
    main()