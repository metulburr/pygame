
import pygame as pg

class ProgressBar:
    def __init__(self, rect, **kwargs):
        
        self.rect = pg.Rect(rect)
        self.maxwidth = self.rect.width
        self.timer = 0.0
        self.time = 1.0
        self.process_kwargs(kwargs)
        if self.text:
            self.text = self.font.render(self.text,True,self.font_color)
    
    def process_kwargs(self,kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {
            'color'      : (0,0,0),
            'bg_color'   : (255,255,255),
            'bg_buff'    : 1,
            'increment'  : 1,
            'progress'   : 0,
            
            'text'       : None,
            'font'       : pg.font.Font(None,16),
            'font_color' : (0,0,0),
            'text_always': False
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("ProgressBar has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)
        
    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.current_time-self.timer > 1000/self.time:
            self.progress += self.increment
            self.timer = self.current_time
        
    def render(self, screen):
        width =  self.progress
        self.complete = False
        if self.progress >= self.maxwidth:
            width = self.maxwidth
            self.complete = True

        pg.draw.rect(screen, self.bg_color, 
            (self.rect.left-self.bg_buff, self.rect.top-self.bg_buff, self.maxwidth+self.bg_buff*2, self.rect.height+self.bg_buff*2))
        pg.draw.rect(screen, self.color, 
            (self.rect.left, self.rect.top, width, self.rect.height))
        if self.text:
            if self.complete or self.text_always:
                text_rect = self.text.get_rect(center=self.rect.center)
                screen.blit(self.text, text_rect)

class Control:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800,600))
        self.done = False
        self.clock = pg.time.Clock()
        
        config = {
            'text'     : 'Progressing',
            'color'    : (200,200,0),
            'bg_color' : (255,255,255),
            'increment'     : 10, 
            'text_always':True
        }
        self.bar = ProgressBar((10,10,100,25), **config)
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
                
    def update(self):
        self.bar.update()
        
    def render(self):
        self.bar.render(self.screen)
        
    def run(self):
        while not self.done:
            self.events()
            self.update()
            self.render()
            pg.display.update()
            self.clock.tick(60)
            
app = Control()
app.run()

