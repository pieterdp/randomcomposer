from couchdb.client import Server, Database
import json
from couchdb.http import ResourceNotFound
from uuid import uuid4
from datetime import datetime


class Cache:
    def __init__(self, db_name):
        server = Server()
        try:
            self.db = server[db_name]
        except ResourceNotFound:
            self.db = server.create(db_name)

    def set(self, doc_id, doc_data):
        dt_now = datetime.now()
        self.db[doc_id] = {
                'data': doc_data,
                'timestamp': dt_now.timestamp()
            }
        return self.db.get(doc_id)['data']

    def get(self, doc_id):
        if self.db.get(doc_id):
            return self.db.get(doc_id)['data']
        else:
            return None

    def mw_set(self, result):
        self.db['composers'] = {'name': result}
        return result

    def mw_get(self):
        try:
            result = self.db['composers']['name']
        except ResourceNotFound:
            result = None
        return result

    def youtube_set(self, composer_name, result):
        self.db[composer_name] = {'result': result}
        return result

    def youtube_get(self, composer_name):
        if self.db.get(composer_name) is not None:
            return self.db.get(composer_name)['result']
        else:
            return None

    def random_set(self, composer_name, result):
        self.db[composer_name] = {'result': result}
        return result

    def random_get(self, composer_name):
        if self.db.get(composer_name) is not None:
            return self.db.get(composer_name)['result']
        else:
            return None
