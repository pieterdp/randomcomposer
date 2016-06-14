from urllib.parse import quote, urljoin
import requests


class ViafApi:
    """
    Query composers. Check whether VIAF has something that looks like
    this composer. If it has, we assume this is a composer. If it hasn't
    we assume it isn't.
    """
    base_url = 'http://www.viaf.org/viaf/AutoSuggest'

    base_params = {}

    def get(self, composer_name):
        return self.query(composer_name)

    def query(self, composer_name):
        url_params = self.base_params
        url_params['query'] = composer_name
        viaf_ids = []
        result = requests.get(self.base_url, url_params)
        if result.status_code >= 400:
            return []
        parsed = result.json()
        if 'result' not in parsed or parsed['result'] is None:
            return []
        for term in parsed['result']:
            if term['nametype'] == 'personal':
                viaf_ids.append((term['viafid'], term['term']))
        return viaf_ids
