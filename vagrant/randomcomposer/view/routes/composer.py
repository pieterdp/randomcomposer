from urllib.parse import quote, unquote

from flask import render_template, session

from randomcomposer import app
from randomcomposer.view.composer.randomview import RandomView


@app.route('/random/composer/choice')
def v_random_composer_choice():
    view = RandomView()
    random_artist = view.random_artist(session=session)
    return render_template('video/list.html', artist={
        'display': random_artist,
        'url_safe': quote(random_artist)
    })


@app.route('/random/composer')
@app.route('/random/composer/')
def v_random_composer():
    view = RandomView()
    random_artist = view.random_artist(session=session)
    embed_link = view.video_embed_link(random_artist)
    return render_template('video/item.html', artist={'display': random_artist}, embed_url=embed_link,
                           title=random_artist)


@app.route('/random/playlist')
@app.route('/random/playlist/')
def v_random_playlist():
    view = RandomView()
    random_artist = view.random_artist(session=session)
    embed_links = view.videos_embed_links(random_artist)
    return render_template('video/items.html', artist={'display': random_artist}, embed_urls=embed_links,
                           title=random_artist)


@app.route('/random/composer/<string:composer_name>/video')
def v_link_composer(composer_name):
    unquoted_composer = unquote(composer_name)
    view = RandomView()
    embed_link = view.video_embed_link(unquoted_composer)
    return render_template('video/item.html', artist={'display': unquoted_composer}, embed_url=embed_link,
                           title=unquoted_composer)


@app.route('/random/composer/<string:composer_name>/playlist')
@app.route('/random/composer/<string:composer_name>/playlist/')
def v_playlist_composer(composer_name):
    unquoted_composer = unquote(composer_name)
    view = RandomView()
    embed_links = view.videos_embed_links(unquoted_composer)
    return render_template('video/items.html', artist={'display': unquoted_composer}, embed_urls=embed_links,
                           title=unquoted_composer)
