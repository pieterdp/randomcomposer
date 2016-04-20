from flask import url_for, redirect, render_template
from randomcomposer.view.web import WebView
from randomcomposer import app


@app.route('/')
def v_index():
    return redirect(url_for('.v_composer'))


@app.route('/composer')
def v_composer():
    wv = WebView()
    music = wv.get_music()
    embed_links = []
    for music_id in music[1]:
        embed_links.append(wv.build_embed_link(music_id))
    return render_template('video/list.html', embed_urls=embed_links, artist=music[0][1])


@app.route('/composer/playlist')
def v_playlist():
    """
    playlist
    Supported players 	HTML5, AS3
    Description 	This parameter specifies a comma-separated list of video IDs to play. If you specify a value,
    the first video that plays will be the VIDEO_ID specified in the URL path, and the videos specified in the playlist
    parameter will play thereafter.
    :return:
    """
    pass


@app.route('/about')
def v_about():
    pass
