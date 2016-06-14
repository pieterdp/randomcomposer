from urllib.parse import quote
import requests
import re
import json


class MwApi:
    composer_pages = ('List of medieval composers', 'List of Renaissance composers', 'List of Baroque composers',
                      'List of Classical-era composers', 'List of Romantic-era composers',
                      'List of 20th-century classical composers', 'List of 21st-century classical composers')
    base_url = 'https://en.wikipedia.org/w/api.php'
    base_params = {
        'action': 'query',
        'prop': 'links',
        'format': 'json'
    }

    def get(self):
        composers = []
        for composer_page in self.composer_pages:
            composers = composers + self.query(composer_page)
        return composers

    def query(self, page_name, plcontinue=None):
        # Exclude lists
        re_list = re.compile('[L|l]ist (of)?')
        # Exclude music of, musical instrument
        re_music = re.compile('[M|m]usic(al)? ')
        composers = []
        url_params = self.base_params
        if plcontinue:
            url_params['plcontinue'] = plcontinue
        url_params['titles'] = page_name
        result = requests.get(self.base_url, params=url_params)
        if result.status_code >= 400:
            return []
        parsed = result.json()
        for page_id, page_data in parsed['query']['pages'].items():
            if int(page_id) < 0:
                break
            if 'links' not in page_data:
                break
            for link in page_data['links']:
                if link['ns'] == 0:
                    if re_list.match(link['title']):
                        continue
                    if re_music.match(link['title']):
                        continue
                    composers.append(link['title'])
        if 'continue' in parsed:
            if 'plcontinue' in parsed['continue']:
                composers = composers + self.query(page_name, plcontinue=parsed['continue']['plcontinue'])
        return composers
