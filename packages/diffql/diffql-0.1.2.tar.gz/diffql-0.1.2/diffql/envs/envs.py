import numpy as np
import gym
from gym import spaces
from typing import Optional


class Clock:
    def __init__(self, max_t, dt, t=0.0, i=0):
        self.t = t
        self.initial_t = self.t
        self.dt = dt
        self.i = i
        self.initial_i = self.i
        self.max_t = max_t

    def tick(self, step=1):
        self.i += step
        self.t += step * self.dt

    def reset(self):
        self.t = self.initial_t
        self.i = self.initial_i

    def current_time(self):
        return self.t

    def is_time_over(self):
        is_time_over = self.t > self.max_t - 0.5*(self.dt)  # for numerical tolerance
        return is_time_over


class AbstractEnv(gym.Env):
    def __init__(self, max_t, dt, t=0.0):
        super().__init__()
        self.clock = Clock(max_t, dt, t=t)

    def reset(self, seed: Optional[int] = None):
        super().reset(seed=seed)
        self.clock.reset()

    def dynamics(self, state, action, time, **kwargs):
        # return should be next_state
        raise NotImplementedError("Implement custom dynamics function")

    def propagate(self, state, action, **kwargs):
        time = self.clock.t
        next_state = self.dynamics(state, action, time, **kwargs)
        self.clock.tick()
        return next_state


class LinearQuadraticDTEnv(AbstractEnv):
    def __init__(self, initial_state, A, B, Q, R, max_t, dt, x_min, x_max, u_min, u_max):
        super().__init__(max_t=max_t, dt=dt)
        if x_min is None:
            x_min = -np.inf * np.ones(self.observation_space_shape)
        if x_max is None:
            x_max = np.inf * np.ones(self.observation_space_shape)
        if u_min is None:
            u_min = -np.inf * np.ones(self.action_space_shape)
        if u_max is None:
            u_max = np.inf * np.ones(self.action_space_shape)
        self.observation_space = spaces.Box(low=x_min, high=x_max, dtype=np.float64)
        self.action_space = spaces.Box(low=u_min, high=u_max, dtype=np.float64)
        self.A = A
        self.B = B
        self.Q = Q
        self.R = R
        self.initial_state = initial_state
        self.state = initial_state

    def dynamics(self, state, action, time=None):
        x = state[:, None]  # reshape to be (n, 1)
        u = action[:, None]  # reshape to be (m, 1)
        x_next = self.A @ x + self.B @ u
        next_state = x_next.reshape(state.shape)
        return next_state

    def reward_function(self, state, action):
        x = state[:, None]  # reshape to be (n, 1)
        u = action[:, None]  # reshape to be (m, 1)
        reward = -(x.T @ self.Q @ x + u.T @ self.R @ u).item()  # to make it float; cost = -reward
        return reward

    def step(self, action):
        state = self.state
        reward = self.reward_function(state, action)

        next_state = self.propagate(state, action)
        self.state = next_state
        done = self.clock.is_time_over() or not self.observation_space.contains(state)  # boolean

        info = {}
        return next_state, reward, done, info

    def reset(self, seed=None):
        super().reset(seed=seed)  # clock, etc.
        self.state = self.initial_state
        return self.state
