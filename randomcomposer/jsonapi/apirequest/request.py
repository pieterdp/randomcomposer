from urllib.parse import quote
from urllib.request import Request, urlopen


class ApiRequest:

    def __init__(self, api_url, url_parameters=None, headers=(), method='GET', body=None):
        self.url = ''
        self.body = ''
        self.method = 'GET'
        self.headers = {}
        self.set_url(api_url, url_parameters)
        self.set_headers(headers)
        self.set_method(method)
        self.set_body(body)
        self.request = self.create_request()

    def set_url(self, base_url, parameters=None):
        """
        Set self.url to the combination of base_url and the parameters.
        parameters is a dict of key, value pairs which will end up
        in the url in the &foo=bar notation.
        The base url contains everything before the first key, value pair (e.g. the "?")
        :param base_url:
        :param parameters:
        :return:
        """
        if parameters is None:
            self.url = '{0}'.format(base_url)
        else:
            param_template = '{0}={1}'
            param_list = []
            for key, value in parameters.items():
                param_list.append(param_template.format(quote(key), quote(value)))
            self.url = '{0}?{1}'.format(base_url, '&'.join(param_list))

    def get_url(self):
        return self.url

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def set_method(self, method):
        """
        Set the HTTP method for the request. If it is not an acceptable HTTP method, it raises an exception.
        :param method:
        :return:
        """
        if method not in ('GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'OPTIONS'):
            raise Exception('Illegal method specified: {0}'.format(method))
        self.method = method

    def get_method(self):
        return self.method

    def set_headers(self, headers=()):
        """
        Set the headers. Supply the headers as a list of tuples of (key, value). Sets 'Content-Type' to
        'application/json' if it wasn't supplied.
        :param headers:
        :return:
        """
        for header in headers:
            self.headers[header[0]] = header[1]
        if 'Content-Type' not in self.headers:
            self.headers['Content-Type'] = 'application/json'

    def get_headers(self):
        return self.headers

    def create_request(self, url=None, url_parameters=None, headers=(), method=None, body=None):
        """
        Create a urllib.Request object with url, headers, method and body. Sets them to
        self.x when they are provided to this function.
        :return Request request:
        """
        if url is not None:
            self.set_url(url, url_parameters)
        if headers is not None:
            self.set_headers(headers)
        if method is not None:
            self.set_method(method)
        if body is not None:
            self.set_body(body)
        if self.body is None:
            request = Request(
                url=self.url,
                headers=self.headers,
                method=self.method
            )
        else:
            request = Request(
                url=self.url,
                data=self.body,
                headers=self.headers,
                method=self.method
            )
        return request

    def set_request(self, request):
        self.request = request

    def execute(self, request=None):
        """
        Perform the request
        :return HTTPResponse:
        """
        if request is not None:
            self.set_request(request)
        return urlopen(self.request)
