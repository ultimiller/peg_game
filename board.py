#!/usr/bin/env python3
import random
import numpy as np

class Board:
    def __init__(self):
        # Create a 5x5 storage, where only a subset of spaces are used.
        # For each space, True = peg, False = no peg, NaN = illegal space
        self.remaining_pegs = 15
        self.move_history = {'first':(-1,-1), 'moves':[]}
        self.spaces = [None] * 5
        for c,_ in enumerate(self.spaces):
            self.spaces[c] = [None] * 5
            for r in range(5):
                if r > c:
                    self.spaces[c][r] = np.nan
                else:
                    self.spaces[c][r] = True
        # Remove the first piece
        self.remove_init_piece()
                    
    
    def remove_init_piece(self):
        done = False
        while done is not True:
            c = random.randrange(start=0, stop=4)
            r = random.randrange(start=0, stop=4)
            done = self.spaces[c][r]
        # Remove the peg in the first legal location found
        self.spaces[c][r] = False
        self.remaining_pegs -= 1
        self.move_history['first'] = (c,r)
        
        
    def update_state(self, move):
            self.spaces[move['start'][0]][move['start'][1]] = False
            self.spaces[move['remove'][0]][move['remove'][1]] = False
            self.spaces[move['end'][0]][move['end'][1]] = True
            self.remaining_pegs -= 1
            self.move_history['moves'].append(move)


    def jump(self):
        '''Find the next move and make a jump
        Return: success     True if a jump could be made, False if there are no
                            more moves
        '''
        moves = []
        # For each space on the board, get the list of legal jumps and add them
        # to the list of possible moves
        for c in range(5):
            for r in range(c+1):
                jumps = self.find_jumps(c, r)
                for j in jumps:
                    moves.append(j)
        if len(moves) == 0:
            return False
        else:
            move_idx = random.randrange(len(moves))
            self.update_state(moves[move_idx])
            return True
            
        
    def find_jumps(self, c, r):
        '''Find the possible jumps starting from [c,r]
        Inputs:
            c       start column
            r       start row
        Outputs:
            jumps   List of legal jumps, each entry is a dict with keys
                    'start', 'end', 'remove'
        '''
        potential = []
        jumps = []
        if self.spaces[c][r] is not True:
            return jumps
        
        # Down, left
        if c+2 < 5:
            potential.append({'remove': (c+1, r), 'end': (c+2, r)})
        # Up, right
        if c-2 >= 0:
            potential.append({'remove': (c-1, r), 'end': (c-2, r)})
        # Down, right
        if c+2 < 5 and r+2 < 5:
            potential.append({'remove': (c+1, r+1), 'end': (c+2, r+2)})
        # Up, left
        if c-2 >= 0 and r-2 >= 0:
            potential.append({'remove': (c-1, r-1), 'end': (c-2, r-2)})
        # Right
        if r+2 < 5:
            potential.append({'remove': (c, r+1), 'end': (c, r+2)})
        # Left
        if r-2 >= 0:
            potential.append({'remove': (c, r-1), 'end': (c, r-2)})
            
        for p in potential:
            if self.spaces[p['remove'][0]][p['remove'][1]] is True:
                if self.spaces[p['end'][0]][p['end'][1]] is False:
                    jumps.append({'start':(c,r), 'end': p['end'], 'remove': p['remove']})
                    
        return jumps
    
    
    def print_move_history(self):
        print("Move History")
        print(f"Initial piece removed: {self.move_history['first']}")
        print("Move\tStart\tEnd")
        for i,m in enumerate(self.move_history['moves']):
            print(f"{i+1}\t{m['start']}\t{m['end']}")
