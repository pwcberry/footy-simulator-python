from dataclasses import dataclass

@dataclass
class TeamScore:
    goals = 0
    behinds = 0
    
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

    For each skill variable, the range is from -0.5 (weak) to 0.5 (strong).

    accuracy: how accurate the unit is at moving the ball forward. For forwards, it indicates how accurate they are at kicking goals
    pressure: how strong the unit is at apply pressure to prevent the ball moving forward (defensive pressure)
    strength: how effective the unit is once they have possesion of the ball (attacking efficiency)
    """
    accuracy: float
    strength: float
    pressure: float


@dataclass
class Team:
    name: str
    forwards: Skills
    mid_field: Skills
    backs: Skills
    ruck: Skills

    # These properties are unused for now
    cohesion: float = 1.0
    fitness: float = 1.0
    health: float = 1.0
