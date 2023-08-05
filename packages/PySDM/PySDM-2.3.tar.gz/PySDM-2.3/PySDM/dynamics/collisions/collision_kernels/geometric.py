"""
basic geometric kernel
"""
from PySDM.physics import constants as const
from PySDM.dynamics.collisions.collision_kernels.impl.gravitational import Gravitational


class Geometric(Gravitational):

    def __init__(self, collection_efficiency=1, x='volume'):
        super().__init__()
        self.collection_efficiency = collection_efficiency
        self.x = x

    def __call__(self, output, is_first_in_pair):
        output.sum(self.particulator.attributes['radius'], is_first_in_pair)
        output **= 2
        output *= const.PI * self.collection_efficiency
        self.pair_tmp.distance(self.particulator.attributes['terminal velocity'], is_first_in_pair)
        output *= self.pair_tmp
