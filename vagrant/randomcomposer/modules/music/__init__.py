import datetime
import re

from randomcomposer.modules.cache import Cache
from randomcomposer.modules.providers.music.youtube import YoutubeApi
from randomcomposer.modules.providers.random.artist import RandomArtist


class Music:
    # TODO support for requery when items is empty => with same parameters, but shorter video length

    def __init__(self):
        self.cache = Cache('random_cache')

    def get(self, input_name, use_last_name_only=True):
        # We only match on the last name
        # This will produce unexpected results for composers that are family.
        if use_last_name_only:
            artist_name = self.get_last_name(input_name)
        else:
            artist_name = input_name
        if not self.cache_valid(artist_name):
            self.to_cache(artist_name)
        cached_item = self.from_cache(artist_name)
        video_ids = self.get_video_ids(cached_item['data'])
        return video_ids

    def get_last_name(self, artist_name):
        """
        Most matches are going to be on the last name of the artist.
        We use the space ( ) as a separator. We assume that
        the first item before the space is the first name, and
        everything else is the last name.
        This will correctly match Ludwig Van Beethoven (looking for Beethoven)
        but utterly fail on Johann Sebastian Bach (looking for Sebastian Bach).
        This is a TODO
        :param artist_name:
        :return:
        """
        space = re.compile(' ')
        names = space.split(artist_name, maxsplit=1)
        if len(names) > 1:
            return names[1]
        else:
            return names[0]

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
        """
        Get the result from the upstream API
        :param artist_name:
        :return:
        """
#        video_sizes = ('long', 'medium', 'short')
#        for video_size in video_sizes:
#            result = self.video_request(artist_name, {'videoDuration': video_size})
#            if len(result['items']) != 0:
#                return result
        return self.video_request(artist_name)

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
