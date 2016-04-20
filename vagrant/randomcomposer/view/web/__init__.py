from randomcomposer.modules.artists import Artists
from randomcomposer.modules.music import Music


class WebView:

    video_url = 'https://www.youtube.com/watch?v={video_id}'
    embed_url = 'http://www.youtube.com/embed/{video_id}'

    def __init__(self):
        self.artists = Artists()
        self.music = Music(self.artists.get())

    def get_music(self, previous_choices=(), debug_artist=None):
        result = self.music.get(previous_choices, debug_artist)
        return result

    def build_video_url(self, video_id):
        return self.video_url.format(video_id=video_id)

    def build_embed_link(self, video_id):
        return self.embed_url.format(video_id=video_id)
