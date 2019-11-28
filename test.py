from gym_antnest.envs.antnest_env import AntNestEnv
import random

def test_antnest():
    env = AntNestEnv()
    env.reset()
    actions = [0,1,2,3]

    for i in range(1500):
        action = random.choice(actions)
        state, reward, done, info = env.step(action)
        env.render()

if __name__ == '__main__':
    test_antnest()