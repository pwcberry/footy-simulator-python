from status import BallDirection, FieldZone, Possession
from matrix import normalise, prob
from direction_matrix import DirectionMatrix

class ForwardsDirectionMatrix(DirectionMatrix):
    def __init__(self, home_team_skill, away_team_skill):
        super().__init__(FieldZone.FORWARDS)

        hst = home_team_skill.strength
        hp = home_team_skill.pressure
        ast = away_team_skill.strength
        ap = away_team_skill.pressure

        self.data[Possession.HOME_TEAM] = dict([
            (BallDirection.NONE, 
                normalise([
                    prob(0.2, hst, 0, ap), prob(0.55, hst, 0, ap),
                    prob(0.05, hst, 0, -ap), prob(0.2, hst, 0, ap)
                ], [0, 1, 2, 3])
            ),
            (BallDirection.FORWARD, 
                normalise([
                    prob(0.05, hst, 0, ap), prob(0.7, hst, 0, ap),
                    prob(0.05, hst, 0, -ap), prob(0.2, hst, 0, ap)
                ], [0, 1, 2, 3])
            ),
            (BallDirection.BACKWARD, 
                normalise([
                    prob(0.1, hst, 0, ap), prob(0.65, hst, 0, ap),
                    prob(0.05, hst, 0, -ap), prob(0.2, hst, 0, ap)
                ], [0, 1, 2, 3])
            ),
            (BallDirection.LATERAL, 
                normalise([
                    prob(0.1, hst, 0, ap), prob(0.6, hst, 0, ap),
                    prob(0.05, hst, 0, -ap), prob(0.25, hst, 0, ap)
                ], [0, 1, 2, 3])
            )
        ])

        self.data[Possession.AWAY_TEAM] = dict([
            (BallDirection.NONE, 
                normalise([
                    prob(0.2, ast, 0, hp), prob(0.5, ast, 0, hp),
                    prob(0.1, ast, 0, -hp), prob(0.2, ast, 0, hp)
                ], [0, 1, 2, 3])
            ),
            (BallDirection.FORWARD, 
                normalise([
                    prob(0.1, ast, 0, hp), prob(0.7, ast, 0, hp),
                    prob(0.1, ast, 0, -hp), prob(0.1, ast, 0, hp)
                ], [0, 1, 2, 3])
            ),
            (BallDirection.BACKWARD, 
                normalise([
                    prob(0.1, ast, 0, hp), prob(0.55, ast, 0, hp),
                    prob(0.15, ast, 0, -hp), prob(0.3, ast, 0, hp)
                ], [0, 1, 2, 3])
            ),
            (BallDirection.LATERAL, 
                normalise([
                    prob(0.1, ast, 0, hp), prob(0.5, ast, 0, hp),
                    prob(0.1, ast, 0, -hp), prob(0.3, ast, 0, hp)
                ], [0, 1, 2, 3])
            )
        ])
