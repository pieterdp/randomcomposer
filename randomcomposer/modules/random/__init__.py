import random


class RandomApi:

    def __init__(self, composers):
        self.max_number = len(composers) - 1
        self.composers = composers

    def get_random(self):
        return random.randrange(0, self.max_number)

    def get_composer(self):
        return self.composers[self.get_random()]
