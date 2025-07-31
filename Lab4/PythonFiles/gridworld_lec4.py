import numpy as np
 

class GridWorld:
    def __init__(self, rows, columns, start_position=None,
            pass_through_reward=0, rewards={}, probs={}):

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

        # probs is a data structure like:
        # {
        #    (pr,pc) : { 'U': { (nr1,nc1): p1, (nr2,nc2): p2, ... }, 'D': ...}
        # }
        # with p1 + p2 + ... = 1

        self.probs = probs

        self.reset()

    def set_state(self, position):
         self.r = position[0]
         self.c = position[1]

    def get_state(self):
        return (self.r, self.c)

    def next_state(self, s, a):
        if s not in self.probs:
           return None

        return self.probs[s].get(a, None)

    def reset(self):
        self.set_state(self.start_position)

    def actions(self, position=None):
        if isinstance(position, type(None)):
            r, c = self.r, self.c
        else:
            r, c = position[0], position[1]
        s = (r, c)

        if s not in self.probs:
            return []

        return list(self.probs[s].keys())

    def move(self, action):
        s = self.r, self.c

        if s not in self.probs:
            raise ValueError('Move not possible')

        if action not in self.probs[s]:
            raise ValueError('Action not possible')

        prob = self.probs[s][action]

        ns = list(prob.keys())
        p = list(prob.values())
        if np.sum(p) != 1.0:
            p[-1] += 1.0 - np.sum(p)

        next_state = ns[np.random.choice(len(ns), p=p)]

        self.r = next_state[0]
        self.c = next_state[1]

        return next_state, self.world[next_state]


    def all_states(self):
      return list(set(self.probs.keys()) | set(self.rewards.keys()))

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
            for c in range(self.columns):
                if s[c] == ' ' and (r, c) not in self.probs:
                    s[c] = 'x'
            print('|' + '|'.join(s) + '|')
            self.print_row()
           

