from gym_antnest.envs.antnest_env import AntNestEnv

def test_antnest():
    env = AntNestEnv()
    env.reset()

    for i in range(600):
        state, reward, done, info = env.step(0)
        env.render()

if __name__ == '__main__':
    test_antnest()