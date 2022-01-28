from matrix import *
from status import FieldZone

class ForwardsMatrix(ZoneMatrix):
    def __init__(self, home_team_skill, away_team_skill, dist):
        super().__init__(FieldZone.FORWARDS)

        hst = home_team_skill.strength
        ha = home_team_skill.accuracy
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        aa = away_team_skill.accuracy
        ap = away_team_skill.pressure

        # C0 = BOUNCE_STATUS
        # C1 = STOPPED_STATUS
        # C2 = THROW_IN_STATUS
        # H0 = HOME_TEAM_OUT_OF_BOUNDS_STATUS
        # H1 = HOME_TEAM_FREE_KICK_STATUS
        # H2 = HOME_TEAM_MOVING_STATUS
        # HB = HOME_TEAM_BEHIND_STATUS
        # HG = HOME_TEAM_GOAL_STATUS
        # A0 = AWAY_TEAM_OUT_OF_BOUNDS_STATUS
        # A1 = AWAY_TEAM_FREE_KICK_STATUS
        # A2 = AWAY_TEAM_MOVING_STATUS

        self.data = dict([
            # [C0, C1, C2, H0, H1, H2, HB, HG, A0, A1, A2]
            # [C0, C1, C2,
            #  H0, H1, H2,
            #  HB, HG,
            #  A0, A1, A2 ]

            (BOUNCE_STATUS,   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (STOPPED_STATUS,  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (THROW_IN_STATUS, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
            (HOME_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
            (HOME_TEAM_FREE_KICK_STATUS,
                normalise([
                    0, prob(0.04, 0, -ha, -hp), 0, 
                    prob(0.04, 0, -ha, -ap), prob(0.01, 0, 0, -hp), prob(0.52, hst, ha, ap),
                    prob_dist(dist, 0.05, 0, ha, ap), prob_dist(dist, 0.07, hst, ha, ap),
                    prob(0.01, 0, -aa, -hp), prob(0.01, ast, 0, -ap), 0
                ], [1, 3, 4, 5, 6, 7, 8, 9])
            ),
            (HOME_TEAM_MOVING_STATUS,
                normalise([
                    0, prob(0.02, 0, -aa, -ap), prob(0.02, 0, -ha, -ap),
                    prob(0.015, 0, -ha, -ap), prob(0.03, hst, 0, -hp), prob(0.2, hst, ha, ap),
                    prob_dist(dist, 0.15, 0, ha, ap), prob_dist(dist, 0.18, hst, ha, ap),
                    prob(0.01, 0, -aa, -hp), prob(0.01, ast, 0, -ap), 0
                ], [1, 2, 3, 4, 5, 6, 7, 8, 9])
            ),
            (HOME_TEAM_BEHIND_STATUS, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
            (HOME_TEAM_GOAL_STATUS,   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (AWAY_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
            (AWAY_TEAM_FREE_KICK_STATUS,
                normalise([
                    0, prob(0.05, 0, -aa, -ap), 0,
                    0, prob(0.015, 0, 0, -hp), 0,
                    0, 0,
                    prob(0.05, 0, -aa, hp), prob(0.01, 0, 0, -ap), prob(0.55, ast, aa, hp)
                ], [1, 4, 8, 9, 10]),

            ),
            (AWAY_TEAM_MOVING_STATUS, 
                normalise([
                    0, prob(0.03, 0, -ha, -ap), prob(0.025, 0, -aa, -hp),
                    prob(0.025, 0, -ha, -ap), prob(0.03, hst, 0, -hp), 0,
                    0, 0,
                    prob(0.025, 0, -aa, -hp), prob(0.04, ast, 0, -hp), prob(0.5, ast, aa, hp)
                ], [1, 2, 3, 4, 8, 9, 10])
            )
        ])