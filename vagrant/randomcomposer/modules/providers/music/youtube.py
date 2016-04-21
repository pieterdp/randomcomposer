import re
from randomcomposer.jsonapi.apirequest.request import ApiRequest
from randomcomposer.jsonapi.apiresponse.response import ApiResponse
from randomcomposer import app


class YoutubeApi:

    best_of = '-best of'
    default_options = {
        'part': 'snippet',
        'type': 'video',
        'key': app.config['API_KEY']
    }
    api_url = 'https://www.googleapis.com/youtube/v3/search'

    def __init__(self, search_term, url_options=None):
        self.search_term = ''
        self.options = {}
        self.request = {}
        self.set_search_term(search_term)
        self.set_options(url_options)
        self.set_request()

    def set_search_term(self, unquoted_term, append_music=True):
        """
        Sets self.search_term to the unquoted search term. Also append '-best of' to
        the search term to prevent Youtube from returning "Best Of" videos (we prefer
        complete musical pieces)
        """
        best_of = re.compile(self.best_of)
        if append_music:
            search_term = '{0} {1}'.format(unquoted_term, 'music')
        else:
            search_term = unquoted_term
        if best_of.search(unquoted_term):
            search_term = '{0}'.format(search_term)
        else:
            search_term = '{0} {1}'.format(search_term, self.best_of)
        self.search_term = search_term

    def get_search_term(self):
        return self.search_term

    def set_options(self, url_params=None):
        """
        Set the options the Youtube API requires/expects. If a required parameter
        is not set, we use self.default_options for that parameter.
        : param url_params: dictionary of URL parameters (key = value)
        :param url_params:
        """
        if url_params is None:
            url_params = {}
        for default_key, default_value in self.default_options.items():
            self.options[default_key] = default_value
        for key, value in url_params.items():
            self.options[key] = value

    def get_options(self):
        return self.options

    def set_request(self, search_term=None, options=None):
        if search_term is not None:
            self.set_search_term(search_term)
        if options is not None:
            self.set_options(options)
        headers = [('Content-Type', 'application/json')]
        youtube_options = self.options
        youtube_options['q'] = self.search_term
        self.request = ApiRequest(
            api_url=self.api_url,
            url_parameters=youtube_options,
            headers=headers,
            method='GET'
        )

    def get_response(self):
        """
        Parse the response from the upstream Youtube API. Returns None if it failed.
        """
        response = ApiResponse(self.request.execute())
        if 200 <= response.get_status() <= 299:
            return response.get_parsed()
        else:
            return None
