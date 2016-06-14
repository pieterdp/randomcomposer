from flask import request, render_template, redirect, url_for, flash, abort, Blueprint
from random import randrange
from randomcomposer.modules.composer import RandomComposer
from randomcomposer.modules.storage import Storage


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/<string:composer_name>/click', methods=['POST'])
def v_api_click(composer_name):
    pass
