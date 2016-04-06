import re
from randomcomposer.jsonapi.apirequest.request import ApiRequest
from randomcomposer.jsonapi.apiresponse.response import ApiResponse


class YoutubeApi:

    best_of = '-best of'
    #https://www.googleapis.com/youtube/v3/search?part=snippet&q=joseph+haydn+-best+of&type=video&videoDuration=long&key={YOUR_API_KEY}
    default_options = {
        'part': 'snippet',
        'type': 'video',
        'videoDuration': 'long'
    }
    api_url = 'https://www.googleapis.com/youtube/v3/search'

    def __init__(self):
        self.search_term = ''
        self.options = {}
        self.request = {}

    def set_search_term(self, unquoted_term):
        """
        Sets self.search_term to the unquoted search term. Also append '-best of' to
        the search term to prevent Youtube from returning "Best Of" videos (we prefer
        complete musical pieces)
        """
        best_of = re.compile(self.best_of)
        if best_of.search(unquoted_term):
            self.search_term = '{0}'.format(unquoted_term)
        else:
            self.search_term = '{0} {1}'.format(unquoted_term, self.best_of)

    def get_search_term(self):
        return self.search_term

    def set_options(self, url_params):
        """
        Set the options the Youtube API requires/expects. If a required parameter
        is not set, we use self.default_options for that parameter.
        : param url_params: dictionary of URL parameters (key = value)
        """
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
            url=self.api_url,
            url_parameters=youtube_options,
            headers=headers,
            method='GET'
        )
