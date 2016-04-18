from randomcomposer.datasource import CategoryMembersApi
from randomcomposer.musicsource.youtube import YoutubeApi
import json
import random


class RandomComposer:

    categories = ['Romantic composers']

    def __init__(self):
        # Assume this is a list of composers
        self.composers = self.get_composers()
        self.random_composer = self.get_random_composer()

    def get_composers(self):
        composers = []
        for category in self.categories:
            mw_categories = CategoryMembersApi('Category:{0}'.format(category))
            composers = composers + mw_categories.chain
        return composers

    def get_random_composer(self, number=None):
        if not number:
            number = random.randint(0, (len(self.composers) - 1))
        return self.composers[number]
