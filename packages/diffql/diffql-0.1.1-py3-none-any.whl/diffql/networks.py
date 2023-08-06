import numpy as np
import math
import torch
import torch.nn as nn
from torch.nn.parameter import Parameter
import torch.nn.init as init
import cvxpy as cp
from cvxpylayers.torch import CvxpyLayer


def construct_layer_list(node_list: list, act):
    """
    Construct a list of layers for feedforward neural networks (FNN).

    node_list: hidden layer nodes ([64, 64, 64])
    act: activation function
    """
    layer_list = nn.ModuleList()  # to be tracked by torch
    for i in range(1, len(node_list)):
        node_prev = node_list[i-1]
        node = node_list[i]
        layer_list.append(nn.Linear(node_prev, node))
        if i is not len(node_list)-1:
            layer_list.append(act)
    return layer_list


class AbstractBivariateApproximator(nn.Module):
    """
    The "bivariate" does not mean that the dimension of the argument of this approximator would be two;
    Instead, it means that the approximator has two arguments as `f(x, u)`.
    """
    def __init__(self):
        super().__init__()

    def minimise_np(self, xs):
        raise NotImplementedError("TODO: for non-parametrised convex approximators, we should add an ad-hoc minimise algorithm.")

    def minimise_tch(self, xs):
        raise NotImplementedError("TODO: for non-parametrised convex approximators, we should add an ad-hoc minimise algorithm.")


class RBFN(AbstractBivariateApproximator):
    """
    Radial basis function network (RBFN).
    It can be used as either univariate or bivariate approximator.

    n: dimension of feature
    l: dimension of output
    N: number of weights
    basis_name: kind of basis function

    basis functions are from scipy:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.Rbf.html
    """
    def __init__(self, centre: torch.Tensor, l: int, basis_name="multiquadric", epsilon: float = None):
        super().__init__()
        # centre
        assert len(centre.shape) == 2
        self.centre = centre  # N x n
        self.N, self.n = self.centre.shape
        self.l = l
        # weight
        weight = torch.empty((self.N, self.l))  # N x l
        # see the source code of torch.nn.modules.linear
        # https://github.com/pytorch/pytorch/blob/master/torch/nn/modules/linear.py
        init.kaiming_uniform_(weight, a=math.sqrt(5))
        self.weight = Parameter(weight)  # RBFN weight
        # basis function
        self.basis_name = basis_name
        self.epsilon = epsilon
        if self.epsilon is None:
            # https://github.com/scipy/scipy/blob/v1.8.0/scipy/interpolate/_rbf.py#L242
            # default epsilon is the "the average distance between nodes" based
            # on a bounding hypercube
            centre_max = np.amax(centre.numpy(), axis=1)
            centre_min = np.amin(centre.numpy(), axis=1)
            edges = centre_max - centre_min
            edges = edges[np.nonzero(edges)]
            self.epsilon = np.power(np.prod(edges)/self.N, 1.0/edges.size)

    def basis_gaussian(self, radii):
        return torch.exp(-(radii/self.epsilon)**2)  # d x N

    def basis_multiquadric(self, radii):
        return torch.sqrt(1 + (radii/self.epsilon)**2)

    def basis_inverse(self, radii):
        return 1.0 / torch.sqrt(1 + (radii/self.epsilon)**2)

    def basis_thin_plate_spline(self, radii):
        return radii**2 * torch.log(radii)

    def basis_bump(self, radii):
        phis = torch.where(self.epsilon*radii < 1,
                           torch.exp(-1/(1 - (self.epsilon*radii)**2)),
                           torch.zeros_like(radii))
        return phis

    def forward(self, xs, *args):
        if len(args) == 1:
            xs = torch.cat((xs, args[0]), axis=1)
        elif len(args) > 1:
            raise ValueError("The number of arguments cannot be more than two.")
        """
        xs: d x n
        radii: d x N
        """
        xss = torch.cat([xs.reshape(*xs.shape, 1)] * self.N, axis=2)  # d x n x N
        xss_shifted = xss - self.centre.T  # d x n x N (broadcasting)
        radii = torch.norm(xss_shifted, dim=1)  # d x N
        if self.basis_name == "gaussian":
            phis = self.basis_gaussian(radii)
        elif self.basis_name == "multiquadric":
            phis = self.basis_multiquadric(radii)
        elif self.basis_name == "inverse":
            phis = self.basis_inverse(radii)
        elif self.basis_name == "thin_plate_spline":
            phis = self.basis_thin_plate_spline(radii)
        elif self.basis_name == "bump":
            phis = self.basis_bump(radii)
        else:
            raise ValueError("Invalid basis function")
        return phis @ self.weight  # d x l


class FNN(AbstractBivariateApproximator):
    def __init__(self, n: int, m: int, _node_list, act):
        super().__init__()
        self.n = n
        self.m = m
        node_list = [n+m, *_node_list, 1]
        self.layer_list = construct_layer_list(node_list, act)

    def forward(self, xs, us):
        zs = torch.cat((xs, us), dim=-1)
        for layer in self.layer_list:
            zs = layer(zs)
        return zs


class AbstractParametrisedConvexApproximator(AbstractBivariateApproximator):
    def __init__(self):
        super().__init__()

    def minimise_np(self, xs):
        raise NotImplementedError("TODO: add cvxpy-like minimise algorithm")

    def minimise_tch(self, xs):
        raise NotImplementedError("TODO: add cvxpylayers-like minimise algorithm")

    def _cvxpylayer_wrapper(self, u, obj, u_min, u_max):
        m = self.m
        constraints = []
        if u_min is not None:
            if u_min is torch.Tensor:
                u_min = u_min.numpy()
            if len(u_min.shape) == 1:
                u_min = u_min.reshape((m,))
            constraints += [u >= u_min]
        if u_max is not None:
            if u_max is torch.Tensor:
                u_max = u_max.numpy()
            if len(u_max.shape) == 1:
                u_max = u_max.reshape((m,))
            constraints += [u <= u_max]
        prob = cp.Problem(obj, constraints)
        cvxpylayer = CvxpyLayer(
            prob,
            parameters=[*self.parameters_cp],
            variables=[u],
        )
        return prob, cvxpylayer

    def initialise_cvxpylayer(self, u_min, u_max):
        m, T, i_max = self.m, self.T, self.i_max
        self.u_cp = cp.Variable((m,))
        alpha_is_u_cp = cp.Parameter((i_max, m))
        beta_is_plus_alpha_is_times_x_cp = cp.Parameter((i_max,))
        self.parameters_cp = [alpha_is_u_cp, beta_is_plus_alpha_is_times_x_cp]
        tmp_cp = self.u_cp @ alpha_is_u_cp.T + beta_is_plus_alpha_is_times_x_cp  # u @ A.T + b
        obj = cp.Minimize(T * cp.log_sum_exp((1/T)*tmp_cp))
        self.prob, self.cvxpylayer = self._cvxpylayer_wrapper(self.u_cp, obj, u_min, u_max)


class ParametrisedConvexApproximator(AbstractParametrisedConvexApproximator):
    def __init__(self, n: int, m: int, i_max: int, node_list, act):
        super().__init__()
        self.n = n
        self.m = m
        self.i_max = i_max
        self.layer_list = construct_layer_list(node_list, act)

    def NN(self, xs):
        for layer in self.layer_list:
            xs = layer(xs)
        return xs


class PLSE(ParametrisedConvexApproximator):
    def __init__(self, n: int, m: int, i_max: int, T: float, _node_list, act, u_min=None, u_max=None):
        node_list = [n, *_node_list, i_max*(m+1)]
        super().__init__(n, m, i_max, node_list, act)
        self.T = T
        self.initialise_cvxpylayer(u_min, u_max)

    def forward(self, xs, us):
        d = xs.shape[0]
        i_max, m, T = self.i_max, self.m, self.T
        X = torch.reshape(self.NN(xs), (d, i_max, m+1))
        alpha_is = X[:, :, 0:-1]  # d x i_max x m
        beta_is = X[:, :, -1]  # d x i_max
        tmp = torch.einsum("bm,bim->bi", us, alpha_is) + beta_is  # each row corresponds to us[i, :] @ alpha_is[i, :, :].T
        return T * torch.logsumexp((1/T)*tmp, dim=-1, keepdim=True)

    def minimise_np(self, x, solver=cp.MOSEK):
        assert type(x) is np.ndarray
        assert len(x.shape) == 1
        i_max, m = self.i_max, self.m
        x = torch.Tensor(x.reshape(1, *x.shape))  # 1 x n
        X = torch.reshape(self.NN(x), (i_max, m+1)).detach().numpy()
        self.parameters_cp[0].value = X[:, 0:-1]  # i_max x m
        self.parameters_cp[1].value = X[:, -1]  # i_max
        self.prob.solve(solver=solver)
        u = self.u_cp.value
        return u

    def minimise_tch(self, xs):
        assert type(xs) is torch.Tensor
        assert len(xs.shape) == 2
        d = xs.shape[0]
        i_max, m = self.i_max, self.m
        X = torch.reshape(self.NN(xs), (d, i_max, m+1))
        alpha_is = X[:, :, 0:-1]  # d x i_max x m
        beta_is = X[:, :, -1]  # d x i_max
        us, = self.cvxpylayer(alpha_is, beta_is)
        return us


class ConvexApproximator(AbstractParametrisedConvexApproximator):
    def __init__(self, n: int, m: int, alpha_is, beta_is):
        """
        alpha_is: i_max x (n+m) Tensor
        beta_is: i_max x (1) Tensor
        """
        super().__init__()
        self.n = n
        self.m = m
        i_max = alpha_is.shape[0]
        assert beta_is.shape[0] == i_max
        assert alpha_is.shape[1] == n + m
        self.i_max = i_max
        self.alpha_is = Parameter(alpha_is)  # torch
        self.beta_is = Parameter(beta_is)  # torch


class LSE(ConvexApproximator):
    def __init__(self, n: int, m: int, i_max: int, T: float, u_min=None, u_max=None):
        assert T > 0
        alpha_is = torch.empty((i_max, n+m))
        beta_is = torch.empty((i_max,))
        # see the source code of torch.nn.modules.linear
        # https://github.com/pytorch/pytorch/blob/master/torch/nn/modules/linear.py
        init.kaiming_uniform_(alpha_is, a=math.sqrt(5))
        fan_in, _ = init._calculate_fan_in_and_fan_out(alpha_is)
        bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
        init.uniform_(beta_is, -bound, bound)
        super().__init__(n, m, alpha_is, beta_is)
        self.T = T
        # cvxpylayer
        self.initialise_cvxpylayer(u_min, u_max)

    def forward(self, xs, us):
        T = self.T
        n = self.n
        alpha_is_u = self.alpha_is[:, n:]
        beta_is_plus_alpha_is_times_x = xs @ self.alpha_is[:, 0:n].T + self.beta_is
        tmp = us @ alpha_is_u.T + beta_is_plus_alpha_is_times_x
        fs = T * torch.logsumexp((1/T)*tmp, dim=-1, keepdim=True)
        return fs

    def minimise_np(self, x, solver=cp.MOSEK):
        assert type(x) is np.ndarray
        assert len(x.shape) == 1
        n = self.n
        alpha_is_u = self.alpha_is[:, n:].detach().numpy()
        beta_is_plus_alpha_is_times_x = x @ self.alpha_is[:, 0:n].T.detach().numpy() + self.beta_is.detach().numpy()
        self.parameters_cp[0].value = alpha_is_u
        self.parameters_cp[1].value = beta_is_plus_alpha_is_times_x
        self.prob.solve(solver=solver)
        u = self.u_cp.value
        return u

    def minimise_tch(self, xs):
        assert type(xs) is torch.Tensor
        assert len(xs.shape) == 2
        d = xs.shape[0]
        n = self.n
        beta_is_plus_alpha_is_times_x = xs @ self.alpha_is[:, 0:n].T + self.beta_is.T  # x A[:, 0:n].T + b.T (d x 1)
        alpha_is_u = self.alpha_is[:, n:]  # A[:, n:]
        us, = self.cvxpylayer(alpha_is_u.repeat(d, 1, 1), beta_is_plus_alpha_is_times_x)
        return us
