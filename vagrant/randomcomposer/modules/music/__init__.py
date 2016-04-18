from randomcomposer.modules.cache import Cache
from randomcomposer.musicsource.youtube.api import YoutubeApi
from randomcomposer.processor.random import RandomArtist
import datetime


class Music:
    def __init__(self, artist_list):
        self.cache = Cache('random_cache')
        self.random = RandomArtist(artist_list)

    def get(self, previous_choices=None):
        if previous_choices:
            artist = self.random.remembered(previous_choices)
        else:
            artist = self.random.simple()
        if not self.cache_valid(artist[1]):
            self.to_cache(artist[1])
        cached_item = self.from_cache(artist[1])
        return cached_item['data']

    def cache_valid(self, artist_name):
        """
        Retrieve the object from the cache and examine its timestamp. If it is more than
        1min in the past, return false
        :return:
        """
        cached_item = self.from_cache(artist_name)
        if cached_item is None:
            return False
        if datetime.datetime.fromtimestamp(cached_item['timestamp']) + datetime.timedelta(minutes=1) < \
                datetime.datetime.now():
            return False
        else:
            return True

    def from_cache(self, artist_name):
        return self.cache.retrieve(artist_name)

    def to_cache(self, artist_name):
        return self.cache.store(self.get_api_result(artist_name), artist_name)

    def get_api_result(self, artist_name):
        yt = YoutubeApi(artist_name)
        return yt.get_response()
