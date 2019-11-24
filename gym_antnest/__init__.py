from gym.envs.registration import register

register(
    id='antnest-v0',
    entry_point='antnest.envs:AntNestEnv',
)
