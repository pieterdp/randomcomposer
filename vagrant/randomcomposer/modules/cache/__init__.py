

class Cache:
    """
    Abstraction layer for a cache storage. Supports ->store(), ->invalidate() and ->retrieve()
    """
    def __init__(self):
        pass

    def store(self, item):
        """
        Stores an item in the cache. The item must be JSON.
        :param item:
        :return:
        """

    def retrieve(self, item_id):
        """
        Retrieve an item from the cache by its ID. The item is returned as JSON.
        :param item_id:
        :return:
        """

    def invalidate(self, item_id):
        """
        Invalidate a single item.
        :param item_id:
        :return:
        """

    def invalidate_all(self):
        """
        Invalidate the entire cache
        :return:
        """
