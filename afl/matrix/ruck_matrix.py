from afl.status import *
from .zone_matrix import ZoneMatrix
from .util import normalise, prob

class RuckZoneMatrix(ZoneMatrix):
    def __init__(self, home_team_skill, away_team_skill):
        super().__init__(FieldZone.RUCK)

        hst = home_team_skill.strength
        ha = home_team_skill.accuracy
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        aa = away_team_skill.accuracy
        ap = away_team_skill.pressure

        # C0 = BOUNCE_STATUS
        # C1 = STOPPED_STATUS
        # C2 = THROW_IN_STATUS
        # H1 = HOME_TEAM_FREE_KICK_STATUS
        # H2 = HOME_TEAM_MOVING_STATUS
        # A1 = AWAY_TEAM_FREE_KICK_STATUS
        # A2 = AWAY_TEAM_MOVING_STATUS

        self.data = dict([
            # [C0, C1, C2, H1, H2, A1, A2]

            # [C0, C1, C2,
            #  H1, H2,
            #  A1, A2]
            (BOUNCE_STATUS,
                normalise([
                    0, 0.05, 0.05,
                    0.025, prob(0.4, hst, ha, ap),
                    0.025, prob(0.4, ast, aa, hp)
                ], [4, 6])
            ),
            (STOPPED_STATUS, [0.9, 0.02, 0.08, 0, 0, 0, 0]),
            (THROW_IN_STATUS, 
                normalise([
                    0, 0.05, 0,
                    0.005, prob(0.4, hst, ha, ap),
                    0.005, prob(0.4, ast, aa, hp)
                ], [4, 6])
            ),
            (HOME_TEAM_FREE_KICK_STATUS, [0, 0, 0, 1, 0, 0, 0]),
            (HOME_TEAM_MOVING_STATUS,    [0, 0, 0, 0, 1, 0, 0]),
            (AWAY_TEAM_FREE_KICK_STATUS, [0, 0, 0, 0, 0, 1, 0]),
            (AWAY_TEAM_MOVING_STATUS,    [0, 0, 0, 0, 0, 0, 1])
        ])

