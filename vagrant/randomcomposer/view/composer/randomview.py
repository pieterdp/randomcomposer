import json
from randomcomposer.modules.artists import Artists
from randomcomposer.modules.music import Music
from randomcomposer.modules.providers.random.artist import RandomArtist


class RandomView:

    embed = 'https://www.youtube.com/embed/{0}'

    def __init__(self):
        self.artist = Artists()
        self.music = Music()

    def random_artist(self, session):
        """
        Return a random artist (as a string)
        :return:
        """
        random = RandomArtist(self.artist.get())
        remembered_choices = self.get_choices_from_session(session)
        random_artist_id, random_artist = random.remembered(previous_choices=remembered_choices)
        self.set_choices_in_session(session, (random_artist_id, random_artist))
        return random_artist

    def video_embed_link(self, artist_name):
        # Get video links
        video_ids = self.music.get(artist_name)
        # Pick the first id, as it is (probably) the most relevant.
        return self.embed.format(video_ids[0])

    def videos_embed_links(self, artist_name):
        video_ids = self.music.get(artist_name)
        embed_links = []
        # We take the first five ID's
        for video_id in video_ids[:5]:
            embed_links.append(self.embed.format(video_id))
        return embed_links

    def get_choices_from_session(self, session):
        """
        Get the previous random artists this user received from the session.
        :param session:
        :return:
        """
        if 'randomcomposer_choices' in session:
            choices_list = json.loads(session['randomcomposer_choices'])
        else:
            choices_list = []
        return choices_list

    def set_choices_in_session(self, session, choice):
        """
        Set this random artist to the session.
        :param session:
        :param choice:
        :return:
        """
        if 'randomcomposer_choices' in session:
            old_list = json.loads(session['randomcomposer_choices'])
        else:
            old_list = []
        old_list.append(choice)
        session['randomcomposer_choices'] = json.dumps(old_list)
