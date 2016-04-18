from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from urllib.parse import quote
# import app


class YoutubeApi:
    def __init__(self):
        # self.api_key = app.config['api_key']
        self.api_key = 'AIzaSyAw16W7kaEMzJg_FyPtQ1U5STeSCuv17dU'
        self.service = build('youtube', 'v3', developerKey=self.api_key)
        #https://www.googleapis.com/youtube/v3/search?part=snippet&q=joseph+haydn&type=video&videoDuration=long
        self.options = {
            'type': 'video',
            'videoDuration': 'long'
        }

    def request_videos(self, composer):
        search_term = quote('{0} -best'.format(composer))
        search = self.service.search().list(part='snippet', q=search_term, type=self.options['type'])
        return search.execute()

    def get_video_list(self, api_response):
        """
        From the api_response, return a list of video ids
        """
        video_list = []
        for result in api_response.get('items', []):
            video_list.append(result['id']['videoId'])
        return video_list
