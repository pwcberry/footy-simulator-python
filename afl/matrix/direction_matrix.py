from afl.status import BallDirection, Possession
from .zone_matrix import ZoneMatrix

class DirectionMatrix(ZoneMatrix):
    def __init__(self, field_zone):
        super().__init__(field_zone)

        self.data[Possession.IN_CONTENTION] = dict([
            (BallDirection.NONE, [1, 0, 0, 0]),
            (BallDirection.FORWARD, [1, 0, 0, 0]),
            (BallDirection.BACKWARD, [1, 0, 0, 0]),
            (BallDirection.LATERAL, [1, 0, 0, 0])
        ])

    @property
    def states(self):
        return [BallDirection.NONE, BallDirection.FORWARD, BallDirection.BACKWARD, BallDirection.LATERAL]

    def row(self, state, possession):
        return self.data[possession][state]
