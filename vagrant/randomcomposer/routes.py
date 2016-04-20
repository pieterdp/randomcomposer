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
    embed_link = wv.build_embed_link(music)
    return render_template('video/list.html', embed_urls=[embed_link])


@app.route('/composer/<string:composer_name>')
def v_specific_composer(composer_name):
    pass


@app.route('/about')
def v_about():
    pass
