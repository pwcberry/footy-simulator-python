# Each matrix row has a base probability. Certain elements in the matrix have a dynamic quality:
# the probability is modified depending on the skill.
# Each row is then normalised to ensure it adds to 1 (to conform to the Markov property).
# The matrix is stored in a dictionary named the `data` field.
class ZoneMatrix:
    def __init__(self, zone):
        self.zone = zone
        self.data = {}

    @property
    def states(self):
        return list(self.data.keys())

    def row(self, state):
        return self.data[state]

