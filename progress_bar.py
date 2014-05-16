
import pygame as pg

class ProgressBar:
    def __init__(self, rect, **kwargs):
        
        self.rect = pg.Rect(rect)
        self.maxwidth = self.rect.width
        self.timer = 0.0
        self.time = 1.0
        self.process_kwargs(kwargs)
        self.complete = False
        if self.text:
            self.text = self.font.render(self.text,True,self.font_color)
    
    def process_kwargs(self,kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {
            'color'      : (0,0,0),
            'bg_color'   : (255,255,255),
            'bg_buff'    : 1,
            'increment'  : 1,
            'percent'   : 0,
            
            'text'       : None,
            'font'       : pg.font.Font(None,20),
            'font_color' : (0,0,0),
            'text_always': False
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)
        
    def progress(self):
        if not self.complete:
            self.percent += self.increment
        #else:
        #    self.percent = 0
        
    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.current_time-self.timer > 1000/self.time: #auto progress
            self.progress() 
            self.timer = self.current_time
        
    def render(self, screen):
        width =  self.percent*self.rect.width/100
        if width >= self.rect.width:
            width = self.rect.width
            self.complete = True
        else:
            self.complete = False
        pg.draw.rect(screen, self.bg_color, 
            (self.rect.left-self.bg_buff, self.rect.top-self.bg_buff, 
            self.rect.width+self.bg_buff*2, self.rect.height+self.bg_buff*2))
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
            'text'       : 'PBar',
            'color'      : (100,100,100),
            'bg_color'   : (255,255,255),
            'increment'  : 25, 
            'text_always': True,
        }
        self.bar = ProgressBar((10,10,100,25), **config)
        self.bar3 = ProgressBar((10,90,50,25), **config)
        self.bar2 = ProgressBar((10,50,200,25), **config)
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.bar2.rect.collidepoint(pg.mouse.get_pos()):
                    self.bar2.progress()
                
    def update(self):
        self.bar.update()
        self.bar2.update()
        self.bar3.update()
        
    def render(self):
        self.bar.render(self.screen)
        self.bar2.render(self.screen)
        self.bar3.render(self.screen)
        
    def run(self):
        while not self.done:
            self.events()
            self.update()
            self.render()
            pg.display.update()
            self.clock.tick(60)
            
app = Control()
app.run()
