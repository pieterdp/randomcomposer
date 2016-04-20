from randomcomposer.modules.cache import Cache
from randomcomposer.datasource.api import MediawikiApi
import json
import datetime


class Artists:
    """
    This class queries the Mediawiki API, gets all the artists from our list of categories
    and stores them in a JSON store so we don't have to query the API every time (this list
    doesn't change very often, so we set the lifetime to 24h)
    """
    categories = ('Category:Baroque composers', 'Category:Classical-period composers', 'Category:Romantic composers')

    def __init__(self):
        self.cache = Cache('randomcomposer')
        self.mw = MediawikiApi()

    def get(self):
        """
        Return a list of artists
        :return:
        """
        if not self.cache_valid():
            self.to_cache()
        cached_item = self.from_cache()
        return cached_item['data']

    def cache_valid(self):
        """
        Retrieve the object from the cache and examine its timestamp. If it is more than
        24h in the past, return false
        :return:
        """
        cached_item = self.from_cache()
        if cached_item is None:
            return False
        if datetime.datetime.fromtimestamp(cached_item['timestamp']) + datetime.timedelta(days=1) <\
                datetime.datetime.now():
            return False
        else:
            return True

    def from_cache(self):
        """
        Get the artist_list item from the cache and return it. It is encoded in JSON,
        so we parse it first.
        :return:
        """
        cached_item = self.cache.retrieve('artist_list')
        return cached_item

    def to_cache(self):
        if self.cache.invalidate('artist_list') is not True:
            raise Exception('Failed to invalidate cache')
        return self.cache.store(self.get_api_result(), 'artist_list')

    def get_api_result(self):
        return self.mw.get_all_pages(categories=self.categories)
