import numpy as np
import pickle

class Player:
    is_training = False
    
    def set_piece(self, piece):
        self.piece = piece
        
    def set_name(self, name):
        self.name = name
        
    def set_board(self, board):
        self.board = board
        
    def set_debug(self, debug):
        self.debug = debug
        
    def update(self):
        pass
    
    def reset(self):
        pass
    
    def set_train(self):
        self.is_training = True
        
    def set_play(self):
        self.is_training = False
        
    def save(self):
        pass
    
    def load(self):
        return self
                       

class Human(Player):
    '''
    Defines a Human player.
    '''
    
    def __init__(self, name):
        self.set_name(name)
        self.set_play()
        
    def play(self):
        '''
        Human player reads in from the keyboard a move and makes a move.

        Returns
        -------
        position : integer
            Valid move from set valid_moves.

        '''
        valid_moves = self.board.valid_moves()
        if self.piece == 1:
            piece = 'x'
        else:
            piece = 'o'
        print(f'player {self.name} ({piece}): {valid_moves}')
        while True:
            position = int(input('position: '))
            if position in valid_moves:
                break
        return position
            
class Random(Player):
    '''
    Defines a Random player.
    '''
    
    def __init__(self, name):
        self.set_name(name)
        
    def play(self):
        '''
        Selects randomly a move from valid_moves.

        Returns
        -------
        a : integer
            Random selection from valid_moves.

        '''
        valid_moves = self.board.valid_moves()
        if not valid_moves:
            print(valid_moves, self.board.board[0])
            self.board.print()
        a = np.random.choice(valid_moves)
        if self.debug: print(f'player {self.name}: {a}')
        return a
    


