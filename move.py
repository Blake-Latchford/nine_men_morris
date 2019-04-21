


class move:
    def __init__(self, board, target, source=None ):
        self.board = board
        self.source = source
        self.target = target
    
    def isValid(self):
        if self.board.phase is board.Phase.place:
            return self._isValidPlacement()
        
        return False
    
    def isValidPlacement(self):
        if self.board.phase is not board.Phase.place:
            return False
        
        if self.source is not None:
            return False
        
        return self.board._rings[self.target[0]][self.target[1]] is board.Player.none

    def createsMill(self):
        if self._createsSpokeMill():
            return True
        
        return self._createsRingMill()
    
    def _createsSpokeMill(self):
        #If the move is on a spoke, look for a mill along it.
        if self.target[1] != self.source[1] and \
                target[1] % board._spoke_period == board._spoke_period - 1:
            for rings_index, ring in enumerate(self.board._rings):
                if rings_index == self.target[0]:
                    continue
                elif ring[self.target[1]] != self.board.turn:
                    break;
            else:
                return True;
                
        return False
        
    def _createsRingMill(self):
        if not source:
            return False
    
        ring = board._rings[self.target[0]]
        
        ring_break_interval = max(board._spoke_period, 2)
        
        # If target[1] is on a corner, then start != mid != end
        # Otherwise we'll duplicate some work.
        start = ((self.target[1] - 1) // ring_break_interval) * ring_break_interval
        mid = (self.target[1] // ring_break_interval) * ring_break_interval
        end = ((self.target[1] + 1) // ring_break_interval) * ring_break_interval
        
        
        adjacent_count = 1;
        for offset in range(1, 3):
            position = self.target[1] + offset
            if ring[position] != self.board.turn:
                break
            if source and source[0] == target[0] and source[1] == position:
                break;
        
        return adjacent_count > 3