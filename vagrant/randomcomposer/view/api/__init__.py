import json
from flask import make_response


class RandomComposerApi:
    def __init__(self, api_class, original_request, api_obj_id=None):
        self.api = api_class()
        self.request = original_request
        self.msg = None
        self.data = u''
        self.response = make_response()
        input_data_raw = self.request.get_data()
        self.input_data = input_data_raw.decode('utf-8')
        if self.request.method == 'GET':
            pass
        elif self.request.method == 'DELETE':
            pass
        elif self.request.method == 'PUT':
            pass
        elif self.request.method == 'POST':
            pass
        else:
            self.msg = 'Unsupported action: {0}'.format(self.request.method)
            self.response.status_code = 405

    def headers(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'

    def create_response(self, data):
        """
        Create a standard API response body
        :param data:
        :return:
        """
        self.response.data = json.dumps({
            'msg': self.msg,
            'data': data
        })
