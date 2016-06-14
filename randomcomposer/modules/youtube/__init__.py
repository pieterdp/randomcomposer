from urllib.parse import quote, urljoin
import requests
import re
import json


class YoutubeApi:
    API_KEY = 'AIzaSyD7V26M-dxNPtUE3_8jVp_eHjI_LerZgwA'

    base_url = 'https://www.googleapis.com/youtube/v3/search'

    embed_url = 'https://www.youtube.com/embed/'

    base_params = {
        'part': 'snippet',
        'maxResults': 15,
        'type': 'video',
        'videoEmbeddable': 'true',
        'key': API_KEY
    }

    def get(self, composer_name):
        url_params = self.base_params
        url_params['q'] = quote(composer_name)
        video_ids = self.query(url_params=url_params)
        embed_urls = []
        for video_id in video_ids:
            embed_urls.append({'id': video_id, 'embed_url': urljoin(self.embed_url, video_id)})
        return embed_urls

    def query(self, url_params, nextPageToken=None):
        result = requests.get(self.base_url, url_params)
        video_ids = []
        if result.status_code >= 400:
            return []
        parsed = result.json()
        if parsed['pageInfo']['totalResults'] == 0:
            return []
        for item in parsed['items']:
            if item['id']['kind'] == 'youtube#video':
                video_ids.append(item['id']['videoId'])
        if len(video_ids) == 0:
            if 'nextPageToken' in parsed:
                video_ids = video_ids + self.query(url_params=url_params, nextPageToken=parsed['nextPageToken'])
        return video_ids
