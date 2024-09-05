import random

class Word:
    MAX_SCORE = 3
    MIN_SCORE = -3

    def __init__(self, word, definitions):
        self.word = word
        self.definitions = definitions
        self.score = 0

    def set_score(self, score):
        self.score = int(score)

    def get_score_str(self):
        return f"{self.word}\t{self.score}\n"

    def is_learned(self):
        return self.score == Word.MAX_SCORE

    def update_correct(self):
        self.score = min(self.score + 1, Word.MAX_SCORE)

    def update_wrong(self):
        self.score = max(self.score - 1, Word.MIN_SCORE)

    def get_random_definition(self):
        return random.choice(self.definitions)