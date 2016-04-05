import json


class ApiResponse:
    def __init__(self, response):
        self.response = None
        self.url = ''
        self.body = ''
        self.status = ''
        self.headers = {}
        self.parsed = {}
        self.set_response(response)
        self.set_url()
        self.set_body()
        self.set_status()
        self.set_headers()
        self.set_parsed()

    def set_response(self, response):
        self.response = response

    def set_url(self):
        """
        Set self.url using geturl from the urllib response object
        :return:
        """
        self.url = self.response.geturl()

    def get_url(self):
        return self.url

    def set_status(self):
        self.status = self.response.getcode()

    def get_status(self):
        return self.status

    def set_headers(self):
        """
        Set self.headers to a dict of key:value from
        response.getheaders(), which returns tuples of (key, value)
        :return:
        """
        for header in self.response.getheaders():
            self.headers[header[0]] = header[1]

    def get_headers(self):
        return self.headers

    def set_body(self):
        self.body = self.response.read()

    def get_body(self):
        return self.body

    def set_parsed(self):
        """
        Parse self.body, which should be a JSON object.
        :return:
        """
        self.parsed = json.loads(self.body)

    def parse(self):
        return self.parsed
