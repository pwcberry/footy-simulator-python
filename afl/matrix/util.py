from math import fsum

def prob(base, strength, accuracy, pressure):
    value = base + base * strength + base * accuracy - base * pressure
    return value if value > 0 else 0


def prob_dist(dist, base, strength, accuracy, pressure):
    # Skill probability
    p = prob(base, strength, accuracy, pressure)

    # Distance probability where distance is 1, 2, or 3
    d = 1 - 0.4 * (dist - 1)
    # d = 0.5 + (2 - distance) * 0.3

    return p + d * p  


def normalise(row, dynamic_indexes):
    prob_sum = fsum(row)

    while prob_sum != 1.0:
        diff = 1.0 - prob_sum
        adjustment = diff / len(dynamic_indexes)

        for i in dynamic_indexes:
            row[i] += adjustment
            if row[i] <= 1e-4:
                row[i] = 0

        prob_sum = fsum(row)
    
    return row
