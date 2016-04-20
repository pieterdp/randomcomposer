import datetime

from randomcomposer.modules.cache import Cache
from randomcomposer.modules.providers.music.youtube import YoutubeApi
from randomcomposer.modules.providers.random.artist import RandomArtist


class Music:
    # TODO support for requery when items is empty => with same parameters, but shorter video length

    def __init__(self, artist_list):
        self.cache = Cache('random_cache')
        self.random = RandomArtist(artist_list)

    def get(self, previous_choices=None, debug_artist=None):
        if previous_choices:
            artist = self.random.remembered(previous_choices)
        else:
            artist = self.random.simple()
        if not self.cache_valid(artist[1]):
            self.to_cache(artist[1])
        cached_item = self.from_cache(artist[1])
        if debug_artist:
            if not self.cache_valid(debug_artist):
                self.to_cache(debug_artist)
            cached_item = self.from_cache(debug_artist)
        video_ids = self.get_video_ids(cached_item['data'])
        return artist, video_ids

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
        if self.cache.invalidate(artist_name) is not True:
            raise Exception('Failed to invalidate cache')
        return self.cache.store(self.get_api_result(artist_name), artist_name)

    def get_api_result(self, artist_name):
        video_sizes = ('long', 'medium', 'short')
        for video_size in video_sizes:
            result = self.video_request(artist_name, {'videoDuration': video_size})
            if len(result['items']) != 0:
                return result

    def video_request(self, artist_name, api_opt=None):
        """
        Helper function to perform requests to the upstream API
        to get a video. Created a helper function so we can
        recurse with e.g. videoDuration options when no results
        are provided.
        :param artist_name:
        :param api_opt:
        :return:
        """
        yt = YoutubeApi(search_term=artist_name, url_options=api_opt)
        return yt.get_response()

    def get_video_ids(self, result):
        ids = []
        for item in result['items']:
            if item['id']['kind'] == 'youtube#video':
                ids.append(item['id']['videoId'])
        return ids
