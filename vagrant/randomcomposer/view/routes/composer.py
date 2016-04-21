from flask import url_for, redirect, render_template, session
import json
from urllib.parse import quote, unquote
from randomcomposer.modules.artists import Artists
from randomcomposer.modules.providers.random.artist import RandomArtist
from randomcomposer import app


def store_previous_choice(choice):
    if 'randomcomposer_choices' in session:
        old_list = json.loads(session['randomcomposer_choices'])
    else:
        old_list = []
    old_list.append(choice)
    session['randomcomposer_choices'] = json.dumps(old_list)


def get_previous_choices():
    if 'randomcomposer_choices' in session:
        choices_list = json.loads(session['randomcomposer_choices'])
    else:
        choices_list = []
    return choices_list


@app.route('/random/composer')
@app.route('/random/composer/')
def v_random_composer():
    artists = Artists()
    random = RandomArtist(artist_list=artists.get())
    remembered_choices = get_previous_choices()
    random_artist = random.remembered(remembered_choices)
    store_previous_choice(random_artist)
    return render_template('video/list.html', artist={
        'display': random_artist[1],
        'url_safe': quote(random_artist[1])
    })


@app.route('/random/composer/<string:composer_name>/link')
def v_link_composer(composer_name):
    unparsed_composer = unquote(composer_name)


@app.route('/random/composer/playlist')
@app.route('/random/composer/playlist/')
def v_playlist():
    pass


@app.route('/random/composer/<string:composer_name>/playlist/')
def v_playlist_composer(composer_name):
    pass
