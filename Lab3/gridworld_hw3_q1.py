import numpy as np
 

class GridWorld:
    def __init__(self, rows, columns, start_position=None,
            pass_through_reward=0, rewards={}, walls={}):

        self.rows = rows
        self.columns = columns
        self.world = pass_through_reward * np.ones((rows, columns))

        if isinstance(start_position, type(None)):
            r = np.random.choice(rows)
            c = np.random.choice(columns)
            start_position = (r, c)
          
        self.start_position = start_position
        self.rewards = rewards

        for position in rewards:
          self.world[position] = rewards[position]

        self.walls = walls

        self.possible_actions = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }

        self.reset()

    def set_state(self, position):
         self.r = position[0]
         self.c = position[1]

    def get_state(self):
        return (self.r, self.c)

    def next_state(self, s, a):
        position = self.get_state()
        self.set_state(s)
        ns, reward = self.move(a)
        self.set_state(position)
        return ns, reward

    def reset(self):
        self.set_state(self.start_position)

    def is_valid_move(self, r, c):
        if r < 0 or r > self.rows-1 or c < 0 or c > self.columns-1:
            return False

        if (r, c) in self.walls:
            return False

        return True


    def actions(self, position=None):
        if isinstance(position, type(None)):
            r, c = self.r, self.c
        else:
            r, c = position[0], position[1]
        possible_moves = []
        for action in self.possible_actions:
            ar, ac = self.possible_actions[action]
            if self.is_valid_move(r + ar, c + ac):
                possible_moves.append(action)

        return possible_moves

    def move(self, action):
        ar, ac = self.possible_actions[action]
        if self.is_valid_move(self.r + ar, self.c + ac):
            self.r += ar
            self.c += ac

        return (self.r, self.c), self.world[self.r, self.c]

    def all_states(self):
      states = []
      for r in range(self.rows):
          for c in range(self.columns):
              if (r, c) not in self.walls:
                  states.append((r, c))
      return states

    def game_over(self):
        return (self.r, self.c) in self.rewards

    def size(self):
        min_size = len(f'{np.min(self.world):.2f}')
        max_size = len(f'{np.max(self.world):.2f}')
        return max(min_size, max_size)

    def print_row(self):
        print('+' + '-+' * self.columns)

    def print(self):

        # +-+-+...+-+
        # |o| |...|g|
        # +-+-+...+-+
        # |x| |...| |
        # +-+-+...+-+

        self.print_row()
        for r in range(self.rows):
            s = [' '] * self.columns
            rp, cp = self.r, self.c
            if r == rp:
                s[cp] = 'o' 
            for reward in self.rewards:
                if r == reward[0]:
                    if self.rewards[reward] > 0:
                        s[reward[1]] = 'G'
                    else:
                        s[reward[1]] = 'B'
            for i in range(len(self.walls)):
                if r == self.walls[i][0]:
                    s[self.walls[i][1]] = 'x'
            print('|' + '|'.join(s) + '|')
            self.print_row()
           

if __name__ == '__main__':
    rewards = {
        (2,0): -100,
        (4,4):  100
    }
    walls = [(2,2), (2,3), (2,4), (3,2)]
    g = GridWorld(5, 5, start_position=(0, 0),
            pass_through_reward=0, rewards=rewards, walls=walls)

    print(g.world)

    while not g.game_over():
        g.print()
        print()

        actions = g.actions()
        print(actions)

        c = ""
        while c not in actions:
            c = input()

        s, reward = g.move(c)

        print(reward)


