from gridworld_lec4 import GridWorld
import numpy as np
import os
 

def GridWorld5x5(p=1):
    rewards = {
        (2,0): -100,
        (4,4):  100
    }
    T = {
        (0,0): { 'R': (0,1), 'D': (1,0) },
        (0,1): { 'R': (0,2), 'L': (0,0), 'D': (1,1) },
        (0,2): { 'R': (0,3), 'L': (0,1), 'D': (1,2) },
        (0,3): { 'R': (0,4), 'L': (0,2), 'D': (1,3) },
        (0,4): { 'L': (0,3), 'D': (1,4) },

        (1,0): { 'R': (1,1), 'D': (2,0), 'U': (0,0) },
        (1,1): { 'R': (1,2), 'L': (1,0), 'D': (2,1), 'U': (0,1) },
        (1,2): { 'R': (1,3), 'L': (1,1), 'U': (0,2) },
        (1,3): { 'R': (1,4), 'L': (1,2), 'U': (0,3) },
        (1,4): { 'L': (1,3), 'U': (0,4) },

        (2,0): { 'R': (2,1), 'D': (3,0), 'U': (1,0) },
        (2,1): { 'L': (2,0), 'D': (3,1), 'U': (1,1) },

        (3,0): { 'R': (3,1), 'D': (4,0), 'U': (2,0) },
        (3,1): { 'L': (3,0), 'D': (4,1), 'U': (2,1) },
        (3,3): { 'R': (3,4), 'D': (4,3) },
        (3,4): { 'L': (3,3), 'D': (4,4) },

        (4,0): { 'R': (4,1), 'U': (3,0) },
        (4,1): { 'R': (4,2), 'L': (4,0), 'U': (3,1) },
        (4,2): { 'R': (4,3), 'L': (4,1) },
        (4,3): { 'R': (4,4), 'L': (4,2), 'U': (3,3) },
        (4,4): { 'L': (4,3), 'U': (3,4) },
    }

    # convert deterministic transition table to stochastic one
    # where we have probability 'p' of leaving the state and
    # probability '1-p' to remain in the same state.

    # this way it is easier to conver the table above to the
    # stochastic version

    for s in T:
        ns_l = list(T[s].values())
        for a in T[s]:
            ns = T[s][a]
            rs = ns_l[np.random.choice(len(ns_l))]
            if ns == rs or p == 1.0:
                T[s][a] = { ns: 1.0 }
            else:
                T[s][a] = { ns: p, rs: np.round(1-p,2) }

    g = GridWorld(5, 5, start_position=(0, 0),
            pass_through_reward=-1, rewards=rewards, probs=T)

    return g


if __name__ == '__main__':

    g = GridWorld5x5(p=0.5)

    print(g.world)

    while not g.game_over():
        g.print()
        print()

        s = g.get_state()

        actions = g.actions()
        print(actions)

        c = ""
        while c not in actions:
            c = input()

        ns, reward = g.move(c)

        print('trying:', g.probs[s][c],
              ' -> action:', c)
        print(reward)


