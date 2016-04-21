from flask import url_for, redirect, render_template
from randomcomposer import app


@app.route('/')
def v_index():
    pass


@app.route('/about')
@app.route('/about/')
def v_about():
    pass
