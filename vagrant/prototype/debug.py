from randomcomposer.musicsource.youtube import YoutubeApi

from randomcomposer.modules.providers.random.artist import RandomComposer

random_composer_c = RandomComposer()
random_composer = random_composer_c.random_composer

yt_api = YoutubeApi()

yt_id_list = yt_api.get_video_list(yt_api.request_videos(random_composer))

print(random_composer)
for yt_id in yt_id_list:
    print('https://www.youtube.com/watch?v={0}'.format(yt_id))