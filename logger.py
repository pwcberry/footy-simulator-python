from status import Timer, GameScore, GameStatus

class GameLog:
    def __init__(self, output):
        self.output = output

    def log_short_score(self, timer: Timer, score: GameScore):
        scores = [(team, score.total()) for team, score in score.current_scores.items()]
        self.output.write("{0} - {1} {2}, {3} {4}\n".format(timer, scores[0][0], scores[0][1], scores[1][0], scores[1][1]))

    def log_full_score(self, score: GameScore):
        self.output.write(score.get_current_score())

    def log_status(self, status: GameStatus):
        s = str(status).replace("GameStatus.", "")
        self.output.write("Status: {}\n".format(s))

    def log_message(self, timer: Timer, message: str):
        self.output.write("{0} - {1}\n".format(timer, message))
