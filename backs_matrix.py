from matrix import *

# def prob_dist(dist, base, strength, accuracy, pressure)
# def prob(base, strength, accuracy, pressure)

class BacksMatrix(Matrix):
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
        # C0M = BACKS_THROW_IN_STATUS
        # H1M = BACKS_HOME_TEAM_STOPPED_STATUS
        # H2M = BACKS_HOME_TEAM_OUT_OF_BOUNDS_STATUS
        # H3M = BACKS_HOME_TEAM_FREE_KICK_STATUS
        # H4M = BACK_HOME_TEAM_MOVING_STATUS
        # A1M = BACKS_AWAY_TEAM_STOPPED_STATUS
        # A2M = BACKS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS
        # A3M = BACKS_AWAY_TEAM_FREE_KICK_STATUS
        # A4M = BACKS_AWAY_TEAM_MOVING_STATUS
        # ABE = BACKS_AWAY_TEAM_BEHIND_STATUS
        # AGO = BACKS_AWAY_TEAM_GOAL_STATUS

        self.data = dict([
            # [C0R, C1R, C2R, C0M, H1M, H2M, H3M, H4M, A1M, A2M, A3M, A4M, ABE, AGO]

            # [C0R, C1R, C2R, C0M,
            #  H1M, H2M, H3M, H4M, 
            #  A1M, A2M, A3M, A4M,
            #  ABE, AGO]
            (RUCK_BOUNCE_STATUS, 
                normalise([
                    0, 0.05, 0.045, 0.005,
                    prob(0.05, hst, 0, ap), prob(0.02, 0, -ha, -ap), 0.01, prob(0.25, hst, ha, ap),
                    prob(0.06, ast, 0, hp), prob(0.01, 0, -aa, -hp), 0.01, prob(0.25, ast, aa, hp),
                    prob_dist(dist, 0.005, ast, 0, hp), prob_dist(dist, 0.005, ast, aa, hp)
                ], [4, 5, 7, 8, 9, 11, 12, 13])),
            (RUCK_STOPPED_STATUS, [0.9, 0.03, 0.07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (RUCK_THROW_IN_STATUS, 
                normalise([
                    0, 0.05, 0, 0.065,
                    prob(0.06, hst, 0, ap), prob(0.01, 0, -ha, -ap), 0.01, prob(0.25, hst, ha, ap),
                    prob(0.06, ast, 0, hp), prob(0.01, 0, -aa, -hp), 0.01, prob(0.25, ast, aa, hp),
                    prob_dist(dist, 0.005, ast, 0, hp), prob_dist(dist, 0.005, ast, aa, hp),
                ], [4, 5, 7, 8, 9, 11, 12, 13])),
            (BACKS_THROW_IN_STATUS,
                normalise([
                    0, 0, 0.088, 0, 
                    0, 0, 0, 0, 
                    0, 0, 0, 0, 
                    prob_dist(dist, 0.005, ast, 0, hp), prob_dist(dist, 0.005, ast, aa, hp)
                ], [12, 13])),
            (BACKS_HOME_TEAM_STOPPED_STATUS, 
                normalise([
                    0, 0, 0, 0.01,
                    prob(0.1, hst, 0, ap), 0, prob(0.05, hst, 0, 0), prob(0.44, hst, ha, ap),
                    prob(0.08, ast, 0, hp), 0, prob(0.02, 0, 0, -ap), prob(0.02, ast, 0, -ap),
                    0, 0
                ], [4, 6, 7, 8, 10, 11])),
            (BACKS_HOME_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
            (BACKS_HOME_TEAM_FREE_KICK_STATUS, 
                normalise([
                    0, 0, 0, 0,
                    prob(0.04, 0, -ha, -hp), prob(0.04, 0, -ha, ap), prob(0.01, 0, 0, -hp), prob(0.55, hst, ha, ap),
                    prob(0.04, 0, -ha, -ap), 0, prob(0.005, 0, 0, -ap), 0,
                    0, 0
                ], [4, 5, 6, 7, 8, 10])),
            (BACKS_HOME_TEAM_MOVING_STATUS, 
                normalise([
                    0, 0, 0, prob(0.025, 0, -ha, -ap),
                    prob(0.03, 0, -aa, -ap), prob(0.015, 0, -ha, -ap), prob(0.03, hst, 0, -hp), prob(0.2, hst, ha, ap),
                    prob(0.02, 0, -ha, -ap), prob(0.01, 0, -aa, -hp), prob(0.01, ast, 0, -ap), 0,
                    0, 0
                ], [4, 5, 6, 7, 8, 9, 10])),
            (BACKS_AWAY_TEAM_STOPPED_STATUS, 
                normalise([
                    0, 0, 0, 0.01,
                    prob(0.08, hst, 0, ap), 0, prob(0.02, 0, 0, -hp), prob(0.02, hst, 0, hp),
                    prob(0.1, ast, 0, hp), 0, prob(0.05, ast, 0, 0), prob(0.44, ast, aa, hp),
                    0, 0
                ], [4, 6, 7, 8, 10, 11])),
            (BACKS_AWAY_TEAM_OUT_OF_BOUNDS_STATUS, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (BACKS_AWAY_TEAM_FREE_KICK_STATUS, 
                normalise([
                    0, 0, 0, 0,
                    prob(0.04, 0, -aa, -hp), 0, prob(0.005, 0, 0, -hp), 0,
                    prob(0.04, 0, -aa, -ap), prob(0.04, 0, -aa, -hp), prob(0.01, 0, 0, -ap), prob(0.52, ast, aa, hp),
                    prob_dist(dist, 0.05, 0, aa, hp), prob_dist(dist, 0.07, ast, aa, hp)
                ], [4, 6, 8, 9, 10, 11, 12, 13])),
            (BACKS_AWAY_TEAM_MOVING_STATUS, 
                normalise([
                    0, 0, 0, prob(0.02, 0, -aa, -hp),
                    prob(0.03, 0, -aa, -hp), prob(0.01, 0, -ha, -ap), prob(0.01, hst, 0, -hp), 0,
                    prob(0.02, 0, -ha, -hp), prob(0.015, 0, -aa, -hp), prob(0.03, ast, 0, -ap), prob(0.2, ast, aa, hp),
                    prob_dist(dist, 0.15, 0, aa, hp), prob_dist(dist, 0.18, ast, aa, hp)
                ], [3, 4, 5, 6, 8, 9, 10, 11, 12, 13])),
            (BACKS_AWAY_TEAM_BEHIND_STATUS, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (BACKS_AWAY_TEAM_GOAL_STATUS, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        ])
