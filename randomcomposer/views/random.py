from flask import request, render_template, redirect, url_for, flash, abort, Blueprint
from random import randrange
from randomcomposer.modules.composer import RandomComposer
from randomcomposer.modules.cache import Cache


composer = Blueprint('composer', __name__, url_prefix='/composer')


@composer.route('/')
def v_random():
    random_composer = RandomComposer()
    composer_data = random_composer.random_composer
    while len(composer_data['youtube_data']) == 0:
        random_composer = RandomComposer()
        composer_data = random_composer.random_composer
    cached_composer = Cache('composer').random_set(composer_data['composer'], composer_data)
    return redirect(url_for('composer.v_random_composer', composer_name=composer_data['composer']))


@composer.route('/<string:composer_name>')
def v_random_composer(composer_name):
    cached_composer = Cache('composer').random_get(composer_name)
    if not cached_composer:
        return redirect(url_for('composer.v_random'))
    if len(cached_composer['youtube_data']) <= 1:
        cached_composer['videos'] = cached_composer['youtube_data']
    else:
        random_start = randrange(0, len(cached_composer['youtube_data']) - 1)
        cached_composer['videos'] = [cached_composer['youtube_data'][random_start]]
    return render_template('list.html', composer=cached_composer)

