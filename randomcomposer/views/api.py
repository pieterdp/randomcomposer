from flask import request, render_template, redirect, url_for, flash, abort, Blueprint
from random import randrange
from randomcomposer.modules.composer import RandomComposer
from randomcomposer.modules.storage import Storage
from randomcomposer.modules.cache import Cache


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/composer/random')
def v_random_composer():
    random_composer = RandomComposer()
    composer_data = random_composer.random_composer
    while len(composer_data['youtube_data']) == 0:
        random_composer = RandomComposer()
        composer_data = random_composer.random_composer
    cached_composer = Cache('composer').random_set(composer_data['composer'], composer_data)


@api.route('/composer/<string:composer_name>')
def v_composer(composer_name):
    pass


@api.route('/composer/<string:composer_name>/tracking', methods=['POST'])
def v_composer_tracking(composer_name):
    pass
