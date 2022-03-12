GAME_TICKS_PER_MINUTE = 10
MINUTES_PER_QUARTER = 20

class Timer:
    minutes = 0
    seconds = 0

    def __init__(self):
        self.reset()

    def tick(self):
        self.seconds += 60 // GAME_TICKS_PER_MINUTE

        if self.seconds >= 60:
            self.minutes += 1
            self.seconds = 0

        if self.minutes > MINUTES_PER_QUARTER:
            self.minutes = MINUTES_PER_QUARTER

    def is_end_of_quarter(self):
        return self.minutes >= MINUTES_PER_QUARTER

    def current_time(self):
        return self.minutes, self.seconds

    def reset(self):
        self.minutes = 0
        self.seconds = 0

    def __repr__(self):
        return "Timer({0:02}, {1:02})".format(self.minutes, self.seconds)

    def __str__(self):
        return "{0:02}:{1:02}".format(self.minutes, self.seconds)
