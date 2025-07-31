import numpy as np
from tqdm import tqdm
from player import Human, Random
import sys

class Board:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.states = [0]
        self.turn = []
        self.actions = []
        self.board = np.zeros((3, 3))
        self.winner = 0
        self.hash_val = 0
        
    def valid_moves(self):
        '''
        Computes all possible moves given current board state.
        
        Returns
        -------
        list
            Possible (r,c) pairs

        '''
        valids = []
        for r in range(3): 
            for c in range(3):
                if not self.board[r,c]:
                    valids.append((r,c))
        return valids
        
    def print(self):
        '''
        Prints board.

        Returns
        -------
        None.

        '''
        board = self.board
        print('Board')
        rows = []
        for r in range(3):
            row = [" "] * 3
            for c in range(3):
                if board[r, c] == 1:
                    row[c] = 'x'
                elif board[r, c] == -1:
                    row[c] = 'o'
            rows.append('|'.join(row) + '\n')
        print('-+-+-\n'.join(rows))
        print()
        
    def step(self, r, c, piece):
        '''
        Places a piece in r, c. 

        Parameters
        ----------
        r : row (0..2)
        c : column (0..2)
        piece : +1/-1
            Piece to be placed.

        Returns
        -------
        None.

        '''
        v = { -1: 2, 1: 1}
        self.board[r,c] = piece
        index = 3 * r + c
        self.hash_val += v[piece] * np.power(3, index)
        self.states.append(self.hash_val)
        self.turn.append(piece)
        self.actions.append((r,c))
            
    def game_over(self):
        '''
        Checks for game over condition, updating winner.

        Returns
        -------
        integer
            Returns 0 for no winner yet, 2 for tie, +1 or -1 for corresponding
            piece.

        '''
        if self.winner != 0: return self.winner

        results = []
        # check rows
        for r in range(3):
            results.append(np.sum(self.board[r]))
        # check columns
        for c in range(3):
            results.append(np.sum(self.board[:, c]))
        # main diagonal
        results.append(self.board[0,0] + self.board[1,1]+self.board[2,2])
        # inverted diagonal
        results.append(self.board[0,2] + self.board[1,1]+self.board[2,0])

        max_results = np.max(results)
        min_results = np.min(results)
        if max_results == 3:
            self.winner = 1
        elif min_results == -3:
            self.winner = -1
        else:
            self.winner = 0
            if np.all(self.board != 0):
                self.winner = 2 # tie
        #if self.winner != 0 and len(self.states) != len(self.actions):
        #    self.turn.append(0)
        #    self.actions.append(-1)
        return self.winner
        
class Game:
    def __init__(self, player1, player2, debug=False):
        self.board = Board()
        self.debug = debug
        self.player1 = player1
        self.player2 = player2
        self.players = { 0: self.player1, 1: self.player2 }
        player1.set_board(self.board)
        player2.set_board(self.board)
        self.state_set = set()
        
    def reset(self):
        '''
        Resets a game, by reseting the board and the players.

        Returns
        -------
        None.

        '''
        self.board.reset()
        self.player1.reset()
        self.player2.reset()
        
    def turn(self, pid):
        '''
        Get next player's id. If current player is 0, next one is 1.

        Parameters
        ----------
        pid : integer in set [0, 1]
            Current player id.

        Returns
        -------
        integer
            Next player's id.

        '''
        return 1 - pid
        
    def play(self):
        '''
        Play a game.

        Returns
        -------
        None.

        '''
        self.reset()
        
        # pick up one of the player's randomly to be the first player
        pid = np.random.choice([0, 1])
        
        # set this player's piece to be 'x'
        self.players[pid].set_piece(1)
        
        # set the other player's piece to be 'o'
        self.players[1-pid].set_piece(-1)
        
        while not self.board.game_over():
            player = self.players[pid]
            
            # play with current player
            r, c = player.play()
            
            # place a piece in that column
            self.board.step(r, c, player.piece)
            
            # update policy and Q/V value functions if player is training.
            if player.is_training:
                player.update()
                
            # get next player
            pid = self.turn(pid)
            
            # print board if we are in debugging mode
            if self.debug:
                self.board.print()
                
        # game is over. print a few statistics in debugging mode.
        if self.debug:
            if self.board.winner == 2:
                print('winner is tie')
            else:
                print('winner is', player.name)
            print('states:', self.board.states)
            print('turns:', self.board.turn)
            print('actions:', self.board.actions)
        
    def train(self, episodes):
        '''
        Trains 'episodes' for the game.

        Parameters
        ----------
        episodes : integer
            Number of episodes to be trained.

        Returns
        -------
        player1_wins : integer
            Number of times player one wins.
        player2_wins : integer
            Number of times player two wins.

        '''
        player1_wins = 0
        player2_wins = 0
        
        # set it to training mode.
        self.player1.set_train()
        self.player2.set_train()
        for _iter in tqdm(range(episodes)):
            # play the game
            self.play()
            
            # let's do a post-training update
            self.player1.update()
            self.player2.update()
            
            # let's update statistics
            if self.player1.piece == self.board.winner:
                player1_wins += 1
            elif self.player2.piece == self.board.winner:
                player2_wins += 1
                
            # let's print from time to time some statistics
            if _iter % 10000 == 0:
                if hasattr(self.player1, 'policy'):
                    n1 = len(self.player1.policy)
                else:
                    n1 = 0
                if hasattr(self.player2, 'policy'):
                    n2 = len(self.player2.policy)
                else:
                    n2 = 0
                p1_msg = f'{self.player1.name}: {player1_wins} ({n1}) / '
                p2_msg = f'{self.player2.name}: {player2_wins} ({n2})'
                tqdm.write(' -> ' + p1_msg + p2_msg)
                
        # after we have finished training, let's save the models.
        player1.save()
        player2.save()
        
        p1_msg = f'{self.player1.name}: {player1_wins} / '
        p2_msg = f'{self.player2.name}: {player2_wins}'
        sys.stdout.flush()
        print(p1_msg + p2_msg)

        return player1_wins, player2_wins
    

def play_against_human(player2):
    '''
    Plays a game against a human.

    Parameters
    ----------
    player2 : Player
        Pre-trained player to play against human.

    Returns
    -------
    None.

    '''
    
    player2.load()
    player2.set_play()
    player1 = Human('H0')
    player1.set_play()
    player2.debug = True
    
    yes = 'Y'
    while yes in ['Y', 'y', 'YES', 'yes']:
        game = Game(player1, player2, debug=True)
        game.play()
                
        yes = input('Do you want to play another game? ')            


if __name__ == '__main__':
    # let's train with two ClaudionorCoelho players
    player2 = Random('R0')
    play_against_human(player2)
