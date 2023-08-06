import numpy as np

from diffql.agents.agents import AbstractAgent
from diffql.networks import AbstractParametrisedConvexApproximator


class ParametrisedConvexQAgent(AbstractAgent):
    def __init__(self, network):
        assert isinstance(network, AbstractParametrisedConvexApproximator)
        self.network = network

    def forward(self, state, time=None, solver=None):
        action = self.network.minimise_np(state, solver=solver)
        return action
