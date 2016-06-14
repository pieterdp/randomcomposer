from flask import Flask


app = Flask(__name__)

from randomcomposer.views.random import composer
app.register_blueprint(composer)
