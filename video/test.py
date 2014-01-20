
import pygame as pg
'''try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
'''

pg.init()
pg.mixer.quit()
#pg.display.init()
filename = 'test-mpeg.mpg'
#f = BytesIO(open(filename, 'rb').read())
movie = pg.movie.Movie(filename)
w, h = movie.get_size()
w = int(w * 1.3 + 0.5)
h = int(h * 1.3 + 0.5)
wsize = (w+10, h+10)
msize = (w, h)
screen = pg.display.set_mode(wsize)
movie.set_display(screen, pg.Rect((5, 5), msize))

pg.event.set_allowed((pg.QUIT, pg.KEYDOWN))
pg.time.set_timer(pg.USEREVENT, 1000)
movie.play()
quit_char = 'q'

while movie.get_busy():
    evt = pg.event.wait()
    if evt.type == pg.QUIT:
        movie.stop()
        break
    elif evt.type == pg.KEYDOWN and evt.unicode == quit_char:
        movie.stop()
        break

pg.time.set_timer(pg.USEREVENT, 0)
pg.quit()
