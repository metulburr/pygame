import pygame as pg

class Control:
    def __init__(self):
        self.screen_size = (600,400)
        self.screen = pg.display.set_mode(self.screen_size)
        self.done = False
        self.pause = False
        
    def run(self):
        while not self.done:
            self.get_events()
            if not self.pause:
                self.update()
                self.render()
                print('executing update functions and render functions')
            else:
                print('pause update and render')
            
    def get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.pause = not self.pause
                
    def update(self):
        pass
        
    def render(self):
        self.screen.fill((0,0,0))
        pg.display.update()

app = Control()
app.run()
