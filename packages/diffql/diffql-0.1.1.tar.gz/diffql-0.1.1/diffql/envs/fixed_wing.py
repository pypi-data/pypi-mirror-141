import numpy as np
from diffql.utils import discretizeContinuousLTI
from diffql.envs.envs import LinearQuadraticDTEnv


class CCVFighterDTLinearEnv(LinearQuadraticDTEnv):
    """
        [Ref.1] B. L. Stevens, F. L. Lewis, E. N. Johson,
        "Modern Design Techniques," in Aircraft Control
        and Simulation: Dynamics, Controls Design,
        and Automation System, 3rd ed. Hoboken,
        New Jersey: John Wiley & Sons, Inc, 2016, pp. 393 - 394
        [Ref.2] Sobel, K.M. and Shapiro, E.Y.,
        "A design methodology for pitch pointing flight control systems,"
        Journal of Guidance, Control, and Dynamics, Vol.8, No.2, pp. 181-187,1985
        doi:10.2514/3.19957
        state = [alpha, q, gamma]
            alpha: angle of attack (rad)
            q: pitch rate (rad/s)
            gamma: flight-path angle (rad)

        input: [delta_e, delta_f]
            delta_e: elevator command (rad) -max. control surface deflection is given by 25 deg
            delta_f: flaperon command (rad) -max. control surface deflection is given by 20 deg
    """
    observation_space_shape = (3,)
    action_space_shape = (2,)
    # plant matrix
    A_c = np.array([
        [-1.341, 0.9933, 0.0],
        [43.223, -0.8693, 0.0],
        [1.341, 0.0067, 0.0],
    ])
    # control matirx
    B_c = np.array([
        [-0.1689, -0.2518],
        [-17.251, -1.5766],
        [0.1689, 0.2518],
    ])

    def __init__(
        self, initial_state=np.zeros(observation_space_shape), dt=0.01, max_t=2.0,
        Q=np.eye(observation_space_shape[0]), R=np.eye(action_space_shape[0]),
        x_min=None, x_max=None, u_min=None, u_max=None,
    ):
        A, B = discretizeContinuousLTI(self.A_c, self.B_c, dt)
        super().__init__(initial_state, A, B, Q, R, max_t, dt, x_min, x_max, u_min, u_max)
