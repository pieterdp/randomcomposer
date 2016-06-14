from randomcomposer.modules.mw import MwApi
from randomcomposer.modules.youtube import YoutubeApi
from randomcomposer.modules.random import RandomApi
from randomcomposer.modules.viaf import ViafApi
from randomcomposer.modules.cache import Cache


class RandomComposer:

    def __init__(self):
        # Get list of composers
        composer_list = self.enwiki()
        self.random_composer = self.get_random(composer_list)

    def get_random(self, composer_list):
        # Get a composer element from the list
        random_api = RandomApi(composer_list)
        random_composer = random_api.get_composer()
        # Check whether the element has a viaf ID (len viaf_ids > 0)
        # If he hasn't, we assume he/she isn't a composer, so we
        # skip him/her
        viaf_ids = self.viaf(random_composer)
        while len(viaf_ids) == 0:
            random_composer = random_api.get_composer()
            viaf_ids = self.viaf(random_composer)
        # Return a list of youtube video urls and ids
        youtube_urls = self.youtube(random_composer)
        return {
            'composer': random_composer,
            'viaf_data': viaf_ids,
            'youtube_data': youtube_urls
        }

    def enwiki(self):
        mw_cache = Cache('enwiki')
        if mw_cache.get('composers'):
            return mw_cache.get('composers')
        else:
            composer_data = MwApi().get()
            return mw_cache.set('composers', composer_data)

    def youtube(self, composer_name):
        yt_cache = Cache('youtube')
        if yt_cache.get(composer_name):
            return yt_cache.get(composer_name)
        else:
            composer_video = YoutubeApi().get(composer_name)
            return yt_cache.set(composer_name, composer_video)

    def viaf(self, composer_name):
        viaf_cache = Cache('viaf')
        if viaf_cache.get(composer_name):
            return viaf_cache.get(composer_name)
        else:
            composer_viaf = ViafApi().get(composer_name)
            return viaf_cache.set(composer_name, composer_viaf)
