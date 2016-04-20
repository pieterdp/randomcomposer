import random


class RandomArtist:

    def __init__(self, artist_list):
        self.artists = artist_list

    def simple(self):
        random_key = random.randint(0, len(self.artists) - 1)
        return random_key, self.artists[random_key]

    def remembered(self, previous_choices):
        """
        Return a random artist, but one that is not in previous_choices.
        previous_choices is a list of (key, artist_name) pairs
        :param previous_choices:
        :return:
        """
        keys = [choice[0] for choice in previous_choices]
        random_key = random.randint(0, len(self.artists) - 1)
        while random_key in keys:
            random_key = random.randint(0, len(self.artists) - 1)
        return random_key, self.artists[random_key]
