from dataclasses import dataclass

@dataclass
class TeamScore:
    goals: int = 0
    behinds: int = 0

    def copy(self):
        return TeamScore(self.goals, self.behinds)

    def total(self):
        return self.goals * 6 + self.behinds  

    def __str__(self):
        return f"{self.goals}. {self.behinds}. {self.total()}"


@dataclass
class Skills:
    """
    The skills that represent a unit within the team.

    accuracy: how accurate the unit is at moving the ball forward. For forwards, it indicates how accurate they are at kicking goals
    pressure: how strong the unit is at apply pressure to prevent the ball moving forward
    strength: how effective the unit is once they have possesion of the ball
    """
    accuracy: float
    pressure: float
    strength: float


@dataclass
class Team:
    name: str
    forwards: Skills
    mid_field: Skills
    backs: Skills
    ruck: Skills
    cohesion: float
    fitness: float
    health: float = 1
