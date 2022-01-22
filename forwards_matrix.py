from matrix import *

class ForwardsMatrix(Matrix):
    def __init__(self, home_team_skill, away_team_skill, dist):
        hst = home_team_skill.strength
        ha = home_team_skill.accuracy
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        aa = away_team_skill.accuracy
        ap = away_team_skill.pressure

        # C0R = RUCK_BOUNCE_STATUS
        # C1R = RUCK_STOPPED_STATUS
        # C2R = RUCK_THROW_IN_STATUS
        # C0M = FORWARDS_THROW_IN_STATUS
        # H1M = FORWARDS_HOME_TEAM_STOPPED_STATUS
        # H2M = FORWARDS_HOME_TEAM_OUT_OF_BOUNDS_STATUS
        # H3M = FORWARDS_HOME_TEAM_FREE_KICK_STATUS
        # H4M = FORWARDS_HOME_TEAM_MOVING_STATUS
        # HBE = FORWARDS_HOME_TEAM_BEHIND_STATUS
        # HGO = FORWARDS_HOME_TEAM_GOAL_STATUS
        # A1M = FORWARDS_AWAY_TEAM_STOPPED_STATUS
        # A2M = FORWARDS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS
        # A3M = FORWARDS_AWAY_TEAM_FREE_KICK_STATUS
        # A4M = FORWARDS_AWAY_TEAM_MOVING_STATUS

        self.data = dict([
            # [C0R, C1R, C2R, C0M, H1M, H2M, H3M, H4M, HBE, HGO, A1M, A2M, A3M, A4M]

            # [C0R, C1R, C2R, C0M, 
            #  H1M, H2M, H3M, H4M,
            #  HBE, HGO,
            #  A1M, A2M, A3M, A4M]
            (RUCK_BOUNCE_STATUS, 
                normalise([
                    0, 0.05, 0.045, 0.005, 
                    prob(0.05, hst, 0, ap), prob(0.02, 0, -ha, -ap), 0.01, prob(0.25, hst, ha, ap),
                    prob_dist(dist, 0.005, hst, 0, ap), prob_dist(dist, 0.005, hst, ha, ap),
                    prob(0.06, ast, 0, hp), prob(0.01, 0, -aa, -hp), 0.01, prob(0.25, ast, aa, hp) 
                ], [4, 5, 7, 8, 9, 10, 11, 13])),
            (RUCK_STOPPED_STATUS, [0.9, 0.03, 0.07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (RUCK_THROW_IN_STATUS, 
                normalise([
                    0, 0.05, 0, 0.065,
                    prob(0.06, hst, 0, ap), prob(0.01, 0, -ha, -ap), 0.01, prob(0.25, hst, ha, ap),
                    prob_dist(dist, 0.005, hst, 0, ap), prob_dist(dist, 0.005, hst, ha, ap),
                    prob(0.06, ast, 0, hp), prob(0.01, 0, -aa, -hp), 0.01, prob(0.25, ast, aa, hp)
                ], [4, 5, 7, 8, 9, 11])),
            (FORWARDS_THROW_IN_STATUS, 
                normalise(
                    [0, 0, 0.088, 0, 
                     0, 0, 0, 0, 
                     prob_dist(dist, 0.005, hst, 0, ap), prob_dist(dist, 0.005, hst, ha, ap), 
                     0, 0, 0, 0], [8, 9])),
            (FORWARDS_HOME_TEAM_STOPPED_STATUS, 
                normalise([
                    0, 0, 0, 0.01,
                    prob(0.1, hst, 0, ap), 0, prob(0.05, hst, 0, 0), prob(0.44, hst, ha, ap),
                    0, 0,
                    prob(0.08, ast, 0, hp), 0, prob(0.02, 0, 0, -ap), prob(0.02, ast, 0, -ap)
                ], [4, 6, 7, 10, 12, 13])),
            (FORWARDS_HOME_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
            (FORWARDS_HOME_TEAM_FREE_KICK_STATUS,
                normalise([
                    0, 0, 0, 0, 
                    prob(0.04, 0, -ha, -hp), prob(0.04, 0, -ha, -ap), prob(0.01, 0, 0, -hp), prob(0.52, hst, ha, ap),
                    prob_dist(dist, 0.05, 0, ha, ap), prob_dist(dist, 0.07, hst, ha, ap),
                    prob(0.04, 0, -ha, -ap), 0, prob(0.005, 0, 0, -ap), 0
                ], [4, 5, 6, 7, 8, 9, 10, 12])),
            (FORWARDS_HOME_TEAM_MOVING_STATUS, normalise([
                    0, 0, 0, prob(0.02, 0, -ha, -ap),
                    prob(0.02, 0, -aa, -ap), prob(0.015, 0, -ha, -ap), prob(0.03, hst, 0, -hp), prob(0.2, hst, ha, ap),
                    prob_dist(dist, 0.15, 0, ha, ap), prob_dist(dist, 0.18, hst, ha, ap),
                    prob(0.03, 0, -ha, -ap), prob(0.01, 0, -aa, -hp), prob(0.01, ast, 0, -ap), 0
                ], [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])),
            (FORWARDS_HOME_TEAM_BEHIND_STATUS, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
            (FORWARDS_HOME_TEAM_GOAL_STATUS, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (FORWARDS_AWAY_TEAM_STOPPED_STATUS, 
                normalise([
                    0, 0, 0, 0.01,
                    prob(0.08, hst, 0, ap), 0, prob(0.02, 0, 0, -hp), prob(0.02, hst, 0, hp),
                    0, 0,
                    prob(0.1, ast, 0, hp), 0, prob(0.05, ast, 0, 0), prob(0.44, ast, aa, hp)
                ], [4, 6, 7, 10, 12, 13])),
            (FORWARDS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (FORWARDS_AWAY_TEAM_FREE_KICK_STATUS, 
                normalise([
                    0, 0, 0, 0,
                    prob(0.08, 0, -aa, -hp), 0, prob(0.015, 0, 0, -hp), 0,
                    0, 0,
                    prob(0.05, 0, -aa, -ap), prob(0.05, 0, -aa, hp), prob(0.01, 0, 0, -ap), prob(0.55, ast, aa, hp)
                ], [4, 6, 10, 11, 12, 13])),
            (FORWARDS_AWAY_TEAM_MOVING_STATUS, 
                normalise([
                    0, 0, 0, prob(0.025, 0, -aa, -hp),
                    prob(0.03, 0, -aa, -hp), prob(0.025, 0, -ha, -ap), prob(0.03, hst, 0, -hp), 0,
                    0, 0,
                    prob(0.03, 0, -ha, -ap), prob(0.025, 0, -aa, -hp), prob(0.04, ast, 0, -hp), prob(0.5, ast, aa, hp)
                ], [3, 4, 5, 6, 10, 11, 12, 13]))
        ])

