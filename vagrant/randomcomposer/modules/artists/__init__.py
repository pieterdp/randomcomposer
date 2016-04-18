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
    categories = ('Category:Baroque_composers', 'Category:Classical-period_composers', 'Category:Romantic_composers')

    def __init__(self):
        self.cache = Cache()

    def get(self):
        """
        Return a list of artists
        :return:
        """

    def cache_valid(self):
        """
        Retrieve the object from the cache and examine its timestamp. If it is more than
        24h in the past, return false
        :return:
        """
        cached_item = self.from_cache()
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
        cached_item_json = self.cache.retrieve('artist_list')
        return json.loads(cached_item_json)
