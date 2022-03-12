from afl.status import *
from .zone_matrix import ZoneMatrix
from .util import normalise, prob

class MidFieldZoneMatrix(ZoneMatrix):
    def __init__(self, home_team_skill, away_team_skill):
        super().__init__(FieldZone.MID_FIELD)

        hst = home_team_skill.strength
        ha = home_team_skill.accuracy
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        aa = away_team_skill.accuracy
        ap = away_team_skill.pressure

        # C1 = STOPPED_STATUS
        # C2 = THROW_IN_STATUS
        # H0 = HOME_TEAM_OUT_OF_BOUNDS_STATUS
        # H1 = HOME_TEAM_FREE_KICK_STATUS
        # H2 = HOME_TEAM_MOVING_STATUS
        # A0 = AWAY_TEAM_OUT_OF_BOUNDS_STATUS
        # A1 = AWAY_TEAM_FREE_KICK_STATUS
        # A2 = AWAY_TEAM_MOVING_STATUS

        self.data = dict([
            # [C1, C2, H0, H1, H2, A0, A1, A2]
            # [C1, C2,
            #  H0, H1, H2,
            #  A0, A1, A2 ]

            (STOPPED_STATUS,  [1, 0, 0, 0, 0, 0, 0, 0]),
            (THROW_IN_STATUS, [0, 1, 0, 0, 0, 0, 0, 0]),
            (HOME_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 0, 0, 1, 0]),
            (HOME_TEAM_FREE_KICK_STATUS, 
                normalise([
                    prob(0.05, 0, -ha, -hp), 0,
                    prob(0.05, 0, -ha, -ap), prob(0.01, 0, 0, -hp), prob(0.55, hst, ha, ap),
                    0, prob(0.015, 0, 0, -ap), 0                    
                ], [0, 2, 3, 4, 6])
            ),
            (HOME_TEAM_MOVING_STATUS,
                normalise([
                    prob(0.03, 0, -aa, -ap), prob(0.025, 0, -ha, -ap),
                    prob(0.025, 0, -ha, -ap), prob(0.04, hst, 0, -hp), prob(0.5, hst, ha, ap),
                    prob(0.025, 0, -aa, -hp), prob(0.03, ast, 0, -ap), 0
                ], [0, 1, 2, 3, 4, 5, 6])),
            (AWAY_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 1, 0, 0, 0, 0]),
            (AWAY_TEAM_FREE_KICK_STATUS,
                normalise([
                    prob(0.05, 0, -aa, -ap), 0,
                    0, prob(0.015, 0, 0, -hp), 0,
                    prob(0.05, 0, -aa, hp), prob(0.01, 0, 0, -ap), prob(0.55, ast, aa, hp)
                ], [0, 3, 5, 6, 7])),
            (AWAY_TEAM_MOVING_STATUS, 
                normalise([
                    prob(0.03, 0, -ha, -ap), prob(0.025, 0, -aa, -hp),
                    prob(0.025, 0, -ha, -ap), prob(0.03, hst, 0, -hp), 0,
                    prob(0.025, 0, -aa, -hp), prob(0.04, ast, 0, -hp), prob(0.5, ast, aa, hp)
                ], [0, 1, 2, 3, 5, 6, 7]))
        ])

