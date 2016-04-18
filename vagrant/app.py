from flask import Flask

app = Flask(__name__)
app.config['API_KEY'] = 'AIzaSyAw16W7kaEMzJg_FyPtQ1U5STeSCuv17dU'

from randomcomposer.musicsource.youtube.api import YoutubeApi
from randomcomposer.datasource.api import MediawikiApi
from randomcomposer.processor.random import RandomArtist

mw = MediawikiApi()

subcats = mw.flatten_subcategory_tree('Category:Baroque composers')

artists = []
for subcat in subcats:
    artists = artists + mw.get_pages(subcat)

ra = RandomArtist(artists)

print(ra.simple()[1])

yt = YoutubeApi(ra.simple()[1])

print(yt.request.execute())