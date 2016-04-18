from randomcomposer import app

from randomcomposer.modules.artists import Artists
from randomcomposer.modules.music import Music

art = Artists()
l = art.get()
mu = Music(l)
print(mu.get())
