import numpy as np
from diffql.envs.envs import LinearQuadraticDTEnv


class MechanicalDTEnv(LinearQuadraticDTEnv):
    """
    [1, Section IV.A]
    [1] G. C. Calafiore and C. Possieri, “Efficient Model-Free Q-Factor Approximation in Value Space via Log-Sum-Exp Neural Networks,” in 2020 European Control Conference (ECC), Saint Petersburg, Russia, May 2020, pp. 23–28. doi: 10.23919/ECC51009.2020.9143765.
    """
    observation_space_shape = (4,)
    action_space_shape = (1,)
    # plant matirx
    A = np.array([
        [0.0289, 0.0010, 0.0475, 0.0019],
        [-3.0836, 0.0226, -6.4323, 0.0442],
        [0.0379, 0.0013, 0.0621, 0.0026],
        [-4.1300, 0.0295, -8.6020, 0.0578],
    ])
    # control matirx
    B = np.array([
        [0],
        [0],
        [0],
        [6.6667],
    ])

    def __init__(
        self, initial_state=np.zeros(observation_space_shape), dt=1, max_t=11,
        Q=np.eye(observation_space_shape[0]), R=np.eye(action_space_shape[0]),
        x_min=None, x_max=None, u_min=None, u_max=None,
    ):
        super().__init__(initial_state, self.A, self.B, Q, R, max_t, dt, x_min, x_max, u_min, u_max)
