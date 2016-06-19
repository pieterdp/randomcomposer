import json
from flask import make_response

##
# (c) 2016 PACKED vzw - GPLv3
# https://github.com/PACKED-vzw/scoremodel/blob/master/scoremodel/modules/api/rest/__init__.py
##


class RestApi:

    def __init__(self):
        self.__response = make_response()

    def response(self, status=None, data=None, msg=None):
        self.__response.data = json.dumps({
            'msg': msg,
            'data': data
        })
        if status:
            self.__response.status_code = status
        else:
            self.__response.status_code = 200
        self.headers()
        return self.__response

    def headers(self):
        self.__response.headers['Content-Type'] = 'application/json'
        self.__response.headers['Access-Control-Allow-Origin'] = '*'
