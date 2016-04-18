from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen
import json


class CategoryMembersApi:
    """
    Get a list of page titles for all pages that are members of a specific MW category.
    https://www.mediawiki.org/wiki/API:Categorymembers
    TODO: support subcategories!
    """

    def __init__(self, category_name):
        self.category_name = quote(category_name)
        self.url_template = \
            'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={0}&cmlimit=500{1}&format=json'
        self.parsed_objects = []
        self.get_all_pages()
        self.chain = self.chain_parsed_objects()

    def create_url(self, continue_from=None):
        """
        Create an URL referring to an API endpoint to get the pages
        from a MW category.
        :param continue_from: if the previous request did not return all category members, use this value to create
                              a &cmcontinue request.
        """
        if continue_from is None:
            url = self.url_template.format(self.category_name, '')
        else:
            url = self.url_template.format(self.category_name, '&cmcontinue={0}'.format(continue_from))
        return url

    def request(self, url):
        """
        Perform a request to the remote.
        """
        try:
            response = urlopen(url)
        except URLError:
            print('Error: {0} returned no response.'.format(url))
            return None
        response_bytes = response.read()
        return response_bytes.decode('utf-8')

    def parse(self, response):
        """
        Parse a response:
        return a list of page_titles and (optionally) a continue_from string if we didn't reach the end of
        the list.
        :param response:
        :return parsed: {
                            'pages' => [],
                            'continue_from' => None|String
                        }
        """
        parsed = {
            'pages': [],
            'continue_from': None
        }
        object_response = json.loads(response)
        if 'query-continue' in object_response:
            parsed['continue_from'] = quote(object_response['query-continue']['categorymembers']['cmcontinue'])
        for page_object in object_response['query']['categorymembers']:
            parsed['pages'].append(page_object['title'])
        return parsed

    def get_all_pages(self, continue_from=None):
        """
        Get all pages in a list by following the cmcontinue parameter, if set. Results are in self.parsed_objects
        :param continue_from:
        TODO: error handling
        """
        url = self.create_url(continue_from)
        response = self.request(url)
        if response is None:
            return None
        parsed_response = self.parse(response)
        self.parsed_objects.append(parsed_response)
        if parsed_response['continue_from'] is not None:
            return self.get_all_pages(continue_from=parsed_response['continue_from'])
        return self.parsed_objects

    def chain_parsed_objects(self):
        """
        Merge all parsed_objects['pages'] into one big array.
        :return chain:
        """
        chain = []
        for parsed_object in self.parsed_objects:
            chain = chain + parsed_object['pages']
        return chain
