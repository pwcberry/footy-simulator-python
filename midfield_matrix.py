from matrix import *
from status import FieldZone

class MidFieldZoneMatrix(ZoneMatrix):
    def __init__(self, home_team_skill, away_team_skill):
        super().__init__(FiledZone.MID_FIELD)

        hst = home_team_skill.strength
        ha = home_team_skill.accuracy
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        aa = away_team_skill.accuracy
        ap = away_team_skill.pressure

        # C0 = STOPPED_STATUS
        # C1 = THROW_IN_STATUS
        # H1M = MID_FIELD_HOME_TEAM_STOPPED_STATUS
        # H2M = MID_FIELD_HOME_TEAM_OUT_OF_BOUNDS_STATUS
        # H3M = MID_FIELD_HOME_TEAM_FREE_KICK_STATUS
        # H4M = MID_FIELD_HOME_TEAM_MOVING_STATUS
        # A1M = MID_FIELD_AWAY_TEAM_STOPPED_STATUS
        # A2M = MID_FIELD_AWAY_TEAM_OUT_OF_BOUNDS_STATUS
        # A3M = MID_FIELD_AWAY_TEAM_FREE_KICK_STATUS
        # A4M = MID_FIELD_AWAY_TEAM_MOVING_STATUS

        # H0 = HOME_TEAM_OUT_OF_BOUNDS_STATUS
        # H1 = HOME_TEAM_FREE_KICK_STATUS
        # H2 = HOME_TEAM_MOVING_STATUS
        # A0 = AWAY_TEAM_OUT_OF_BOUNDS_STATUS
        # A1 = AWAY_TEAM_FREE_KICK_STATUS
        # A2 = AWAY_TEAM_MOVING_STATUS


        self.data = dict([
            # [C0R, C1R, C2R, C0M, H1M, H2M, H3M, H4M, A1M, A2M, A3M, A4M]

            # [C0R, C1R, C2R, C0M,
            #  H1M, H2M, H3M, H4M, 
            #  A1M, A2M, A3M, A4M]
            (RUCK_BOUNCE_STATUS, 
                normalise([
                    0, 0.05, 0.05, 0.01, 
                    prob(0.05, hst, 0, ap), prob(0.02, 0, -ha, -ap), 0.01, prob(0.2, hst, ha, ap), 
                    prob(0.05, ast, 0, hp), prob(0.02, 0, -aa, -hp), 0.1, prob(0.2, ast, aa, hp)
                ], [4, 5, 7, 8, 9, 11])),
            (RUCK_STOPPED_STATUS, [0.9, 0.03, 0.07, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (RUCK_THROW_IN_STATUS, 
                normalise([
                    0, 0.05, 0, 0.08,
                    prob(0.06, hst, 0, ap), prob(0.01, 0, -ha, -ap), 0.01, prob(0.25, hst, ha, ap),
                    prob(0.06, ast, 0, hp), prob(0.01, 0, -aa, -hp), 0.01, prob(0.25, ast, aa, hp)
                ], [4, 5, 7, 8, 9, 11])),
            (MID_FIELD_THROW_IN_STATUS, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (MID_FIELD_HOME_TEAM_STOPPED_STATUS,
                normalise([
                    0, 0, 0, 0.01,
                    prob(0.1, hst, 0, ap), 0, prob(0.05, hst, 0, 0), prob(0.44, hst, ha, ap),
                    prob(0.08, ast, 0, hp), 0, prob(0.02, 0, 0, -ap), prob(0.02, ast, 0, -ap)
                ], [4, 6, 7, 8, 10, 11])),
            (MID_FIELD_HOME_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
            (MID_FIELD_HOME_TEAM_FREE_KICK_STATUS,
                normalise([
                    0, 0, 0, 0, 
                    prob(0.05, 0, -ha, -hp), prob(0.05, 0, -ha, -ap), prob(0.01, 0, 0, -hp), prob(0.55, hst, ha, ap),
                    prob(0.08, 0, -ha, -ap), 0, prob(0.015, 0, 0, -ap), 0
                ], [4, 5, 6, 7, 8, 10])),
            (MID_FIELD_HOME_TEAM_MOVING_STATUS,
                normalise([
                    0, 0, 0, prob(0.025, 0, -ha, -ap),
                    prob(0.03, 0, -aa, -ap), prob(0.025, 0, -ha, -ap), prob(0.04, hst, 0, -hp), prob(0.5, hst, ha, ap),
                    prob(0.03, 0, -ha, -ap), prob(0.025, 0, -aa, -hp), prob(0.03, ast, 0, -ap), 0
                ], [3, 4, 5, 6, 7, 8, 9, 10])),
            (MID_FIELD_AWAY_TEAM_STOPPED_STATUS,
                normalise([
                    0, 0, 0, 0.01,
                    prob(0.08, hst, 0, ap), 0, prob(0.02, 0, 0, -hp), prob(0.02, hst, 0, hp), 
                    prob(0.1, ast, 0, hp), 0, prob(0.05, ast, 0, 0), prob(0.44, ast, aa, hp)
                ], [4, 6, 7, 8, 10, 11])),
            (MID_FIELD_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
            (MID_FIELD_AWAY_TEAM_FREE_KICK_STATUS, 
                normalise([
                    0, 0, 0, 0,
                    prob(0.08, 0, -aa, -hp), 0, prob(0.015, 0, 0, -hp), 0,
                    prob(0.05, 0, -aa, -ap), prob(0.05, 0, -aa, hp), prob(0.01, 0, 0, -ap), prob(0.55, ast, aa, hp)
                ], [4, 6, 8, 9, 10, 11])),
            (MID_FIELD_AWAY_TEAM_MOVING_STATUS, 
                normalise([
                    0, 0, 0, prob(0.025, 0, -aa, -hp),
                    prob(0.03, 0, -aa, -hp), prob(0.025, 0, -ha, -ap), prob(0.03, hst, 0, -hp), 0,
                    prob(0.03, 0, -ha, -ap), prob(0.025, 0, -aa, -hp), prob(0.04, ast, 0, -hp), prob(0.5, ast, aa, hp)
                ], [3, 4, 5, 6, 8, 9, 10, 11]))
        ])

