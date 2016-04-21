from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

import randomcomposer.view.routes.public
import randomcomposer.view.routes.composer
