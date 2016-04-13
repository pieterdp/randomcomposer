import re
from randomcomposer.jsonapi.apirequest.request import ApiRequest
from randomcomposer.jsonapi.apiresponse.response import ApiResponse


class MediawikiApi:
    """
    API that interfaces with the English Wikipedia API to get a list of all classical composers.
    It does this by querying the following categories:
        https://en.wikipedia.org/wiki/Category:Baroque_composers (1600 - 1760)
        https://en.wikipedia.org/wiki/Category:Classical-period_composers (1760 - 1820)
        https://en.wikipedia.org/wiki/Category:Romantic_composers (1820 - 1910)
    We also query subcategories
    https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={0}&cmlimit=500{1}&format=json
    """

    composer_cat = (
        'Baroque composers',
        'Classical-period composers',
        'Romantic composers'
    )
    api_url = 'https://en.wikipedia.org/w/api.php'
    default_options = {
        'action': 'query',
        'list': 'categorymembers',
        'cmlimit': '500',
        'format': 'json'
    }

    def __init__(self, api_url=None, api_options=None):
        self.url = ''
        self.options = {}
        if api_url is None:
            api_url = self.api_url
        self.set_url(api_url)
        self.set_options(api_options)

    def set_url(self, api_url):
        self.url = api_url

    def get_url(self):
        return self.url

    def set_options(self, url_params=None):
        """
        Set the options the MW API requires/expects. If a required parameter
        is not set, we use self.default_options for that parameter.
        : param url_params: dictionary of URL parameters (key = value)
        """
        if url_params is None:
            url_params = {}
        for default_key, default_value in self.default_options.items():
            self.options[default_key] = default_value
        for key, value in url_params.items():
            self.options[key] = value

    def get_options(self):
        return self.options

    def get_items(self, category_name, url_options=None, continue_from=None):
        """
        Abstract function that gets all items in a given category. By default it fetches
        the pages, but you can add a parameter to url_options to get the subcategory (or another
        parameter for something else, see Mediawiki:API).
        If continue_from is set, we are expanding a request (we get by default only the first 500 items):
            add this parameter to the url_options as cmcontinue.
        If we find continue in the result, we call ourselves with continue_from set to the value of continue.cmcontinue
        In case of failure, we return the items array (which will be empty if we
         get an error on the first pass) and print that the upstream returned an error.
        :param category_name:
        :param url_options:
        :param continue_from:
        :return:
        """
        items = []
        options = {'cmtitle': category_name}
        if url_options is not None:
            for key, value in url_options.items():
                options[key] = value
        if continue_from is not None:
            options['cmcontinue'] = continue_from
        upstream_response = self.perform_request(options)
        if not (200 <= upstream_response.get_status() <= 299):
            print('The remote returned an error: {0}'.format(upstream_response.get_status()))
            return items
        items.append(upstream_response.get_parsed())
        if 'continue' in upstream_response.get_parsed():
            items = items + self.get_items(category_name,
                                           continue_from=upstream_response.get_parsed()['continue']['cmcontinue'],
                                           url_options=url_options)
        return items

    def get_pages(self, category_name):
        """
        Get all pages in a given category.
        :param category_name:
        :return:
        """
        items = self.get_items(category_name)
        pages = []
        for item in items:
            for page_object in item['query']['categorymembers']:
                pages.append(page_object['title'])
        return pages

    def get_subcategories(self, category_name):
        """
        Get all subcategories for a given category. We get the parsed return value from the API.
        The information we want is in query.categorymembers
        """
        items = self.get_items(category_name, url_options={'cmtype': 'subcat'})
        subcategories = []
        for item in items:
            for sub_cat_object in item['query']['categorymembers']:
                subcategories.append(sub_cat_object['title'])
        return subcategories

    def flatten_subcategory_tree(self, parent_category):
        """
        For a given parent_category, walk the tree of its subcategories and return
        them as a flat list.
        We limit the recursion to one level because the category tree can become
        very deep if a famous composer gets his own category. We'll be looking at
        musical pieces instead of composers.
        We have a 'template' category in our tree. Those are internal MW templates,
        not composers. We skip them as well using a regular expression.
        """
        subcategories = []
        template = re.compile('template')
        subs_from_parent = self.get_subcategories(parent_category)
        if len(subs_from_parent) != 0:
            for sub_cat in subs_from_parent:
                if not template.search(sub_cat):
                    subcategories.append(sub_cat)
        return subcategories

    def perform_request(self, additional_opts=None):
        """
        Perform a request to the upstream API. You can override the options
        in self.options by specifying them in additional_opts
        """
        options = self.options
        if additional_opts is not None:
            for key, value in additional_opts.items():
                options[key] = value
        request = ApiRequest(self.url, url_parameters=options)
        response = ApiResponse(request.execute())
        return response
