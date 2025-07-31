import gymnasium as gym

is_pong = False
#env = gym.make('Pong-ram-v0', render_mode='human'); is_pong = True
#env = gym.make('Pong-v0', render_mode='human'); is_pong = True
env = gym.make('Pitfall-v0', render_mode='human'); is_pong = True

for i_episode in range(10):
    observation = env.reset()
    #print(observation); exit()
    done = False
    t = 0
    scores = {-1.0: 0, 1.0: 0}
    while not done:
        action = env.action_space.sample()
        observation, reward, done, truncated, info = env.step(action)
        t += 1
        if is_pong:
            if reward != 0.0: scores[reward] += 1
        if scores[-1.0] + scores[1.0] > 6 and not done:
            import pdb; pdb.set_trace()
        if done:
            print(f'Episode finished after {t+1} steps', end='')
            if is_pong:
                print(f' - score: {scores[-1.0]} x {scores[1.0]}')
            break
env.close()



