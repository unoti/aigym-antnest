# aigym-antnest
Multi-agent Ant Nest Simulation Environment for Open AI Gym


## Installation
 1. Clone the repo
    ```
    git clone git@github.com:unoti/aigym-antnest.git
    ```
 2. ```cd``` into ```aigym-antnest``` and run:

    ```pip install -e .```

## Try it
This will run 100 instances of the antnest environment for 1000 timesteps.  You should see a window pop up rendering the simulation world.

```python
import gym
import antnest

env = gym.make('antnest-v0')

for i in range(100):
    env.reset()
    for t in range(1000):
        env.render()
        observation, reward, done, info = env.step(env.action_space.sample())
        if done:
            print('episode {} finished after {} timesteps'.format(i, t))
            break
```