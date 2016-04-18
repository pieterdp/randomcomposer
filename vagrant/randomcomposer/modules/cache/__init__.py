import datetime
from pymongo import MongoClient


class Cache:
    """
    Abstraction layer for a cache storage. Supports ->store(), ->invalidate() and ->retrieve()
    """
    def __init__(self, collection=None):
        client = MongoClient()
        self.db = client.randomcomposer
        if collection is None:
            self.collection = self.db.default
        else:
            self.collection = self.db[collection]

    def store(self, item, item_id=None):
        """
        Stores an item in the cache. The item must be JSON-serialisable. If you want to set the item_id explicitly,
        that is possible. Returns the ID of the stored item or throws an Exception on failure.
        :param item:
        :param item_id:
        :return:
        """
        wrapped = self.wrap_object(item)
        if item_id is not None:
            wrapped['_id'] = item_id
        stored = self.collection.insert_one(wrapped)
        return stored.inserted_id

    def retrieve(self, item_id):
        """
        Retrieve an item from the cache by its ID. The item is returned as unserialised JSON. Returns None
        if nothing was found.
        :param item_id:
        :return:
        """
        return self.collection.find_one({'_id': item_id})

    def invalidate(self, item_id):
        """
        Invalidate a single item.
        :param item_id:
        :return:
        """
        if self.collection.delete_one({'_id': item_id}):
            return True
        return False

    def invalidate_all(self):
        """
        Invalidate the entire cache
        :return:
        """
        return self.collection.remove({})

    def wrap_object(self, object_to_cache):
        dt_now = datetime.datetime.now()
        return {
            'timestamp': dt_now.timestamp(),
            'data': object_to_cache
        }
