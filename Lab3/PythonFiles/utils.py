from gridworld_hw3_q1 import GridWorld
import numpy as np

def get_size(V):
    if isinstance(V, dict):
        V = list(V.values())
    min_size = len(f'{np.min(V):.2f}')
    max_size = len(f'{np.max(V):.2f}')
    return max(min_size, max_size)

 
def print_row(columns, size=4):
    print('+' + ('-'*size + '+') * columns)


def print_policy(policy, gw, size):
    size_l = size // 2
    size_r = size - size_l - 1
    print_row(gw.columns, size)
    for r in range(gw.rows):
        s = []
        for c in range(gw.columns):
            s.append(' ' * size_l + policy.get((r, c), ' ') + ' ' * size_r)
        print('|' + '|'.join(s) + '|')
        print_row(gw.columns, size)


def print_value(V, gw, size):
    print_row(gw.columns, size)
    for r in range(gw.rows):
        s = []
        for c in range(gw.columns):
            v = f'{V.get((r, c), 0):.2f}'
            v_diff = len(v)
            s.append(' ' * (size - v_diff) + v)
        print('|' + '|'.join(s) + '|')
        print_row(gw.columns, size)


if __name__ == '__main__':
    rewards = {
        (2,0): -100,
        (4,4):  100
    }
    walls = [(2,2), (2,3), (2,4), (3,2)]
    g = GridWorld(5, 5, start_position=(0, 0),
            pass_through_reward=0, rewards=rewards, walls=walls)

    policy = {}
    V = {}
    for state in g.all_states():
        policy[state] = np.random.choice(g.actions(state))
        V[state] = np.random.randn()

    print_policy(policy, g, size=get_size(V))
    print_value(V, g, size=get_size(V))
 
