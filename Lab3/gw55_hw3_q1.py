from gridworld_hw3_q1 import GridWorld
import numpy as np
import os
 

def GridWorld5x5():
    rewards = {
        (2,0): -100,
        (4,4):  100
    }

    walls = [(2,2), (2,3), (2,4), (3,2)]

    g = GridWorld(5, 5, start_position=(0, 0),
            pass_through_reward=0, rewards=rewards, walls=walls)

    return g


if __name__ == '__main__':

    g = GridWorld5x5()

    print(g.world)

    while not g.game_over():
        g.print()
        print()

        actions = g.actions()
        print(actions)

        c = ""
        while c not in actions:
            c = input()

        s, r = g.move(c)

        reward = g.world[s]

        print(s, reward)

