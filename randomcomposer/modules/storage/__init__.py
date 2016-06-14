from couchdb.client import Server, Database
import json
from couchdb.http import ResourceNotFound
from uuid import uuid4
from datetime import datetime


class Storage:

    def __init__(self):
        server = Server()
        try:
            self.db = server['randomcomposer']
        except ResourceNotFound:
            self.db = server.create('randomcomposer')

    def store(self, composer_name):
        document = {
            'name': composer_name,
            'clicks': 0
        }
        self.db[composer_name] = document
        return document

    def get(self, composer_name):
        try:
            document = self.db[composer_name]
        except ResourceNotFound:
            document = None
        return document

    def add_click(self, composer_name):
        document = self.get(composer_name)
        if document is None:
            return None
        else:
            document['clicks'] += 1
            self.db[composer_name] = document
        return document['clicks']
