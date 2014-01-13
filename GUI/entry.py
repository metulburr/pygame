



import pygame as pg
import os
        
class Entry:
    instances = []
    def __init__(self, text='', width=100, height=10, **kwargs):
        Entry.instances.append(self)
        self.assign_kwargs(kwargs)
        self.text = text
        self.label, self.label_rect = self.render_font(self.text, self.font, self.fontsize)
        self.color = self.bg_color
        
        self.image = pg.Surface([width,height]).convert()
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()
        self.label_rect.center = self.rect.center
        self.focus = False
        
    def assign_kwargs(self, kwargs):
        self.hover_bg_color = kwargs['hover']
        self.bg_color = kwargs['bg']
        self.text_color = kwargs['fg']
        self.font = kwargs['font']
        #self.border = kwargs['border']
        self.fontsize = kwargs['fontsize']
        
    def render_font(self, text, filename, size):
        if not filename:
            f = pg.font.SysFont('Arial', size)
        else:
            f = Font.load(self.font, size)
        font = f.render(text, 1, self.text_color)
        rect = font.get_rect()
        return (font, rect)
        
    def render(self, screen):
        pg.draw.rect(screen, self.color, self.rect, False)
        screen.blit(self.label, self.label_rect)
        
    def mouse_collision(self):
        if self.focus:
            self.color = self.hover_bg_color
        else:
            self.color = self.bg_color
            
    def update(self):
        self.label_rect.left = self.rect.left
        self.label_rect.centery = self.rect.centery
        self.mouse_collision()
        
    def get_event(self, event):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for obj in Entry.instances: 
                    obj.focus = False
                self.focus = not self.focus
        if event.type == pg.KEYDOWN:
            if self.focus:
                if event.unicode.isprintable():
                    self.text += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_DELETE:
                    self.text = ''
                self.label, self.label_rect = self.render_font(self.text, self.font, self.fontsize)
            

if __name__ == "__main__":
        
    class Font:
        '''simulating tools'''
        path = 'resources/fonts'
        @staticmethod
        def load(filename, size):
            p = os.path.join(Font.path, filename+'.ttf')
            return pg.font.Font(os.path.abspath(p), size)

    def callback():
        print('running callback')
        
    def callback2():
        print('running callback 2')
        
    class Control:
        def __init__(self):
            pg.init()
            self.screen = pg.display.set_mode((800,600))
            self.screen_rect = self.screen.get_rect()
            self.Clock = pg.time.Clock()
            self.done = False
            
            self.button_settings = {
                'hover'   : (255,255,255),
                'font'    : 'impact',
                'fg'      : (0,0,0),
                'bg'      : (155,155,155),
                'border'  : False,
                'fontsize': 15
            }
            
            self.e = Entry(text='default text', width=100, height=20, **self.button_settings)
            self.e.rect.center = (200,100)
            self.e2 = Entry(text='default text', width=100, height=20, **self.button_settings)
            self.e2.rect.center = (200,150)
            self.e3 = Entry(text='default text', width=100, height=20, **self.button_settings)
            self.e3.rect.center = (200,200)
            self.buttons = [self.e, self.e2, self.e3]
            
        def event_loop(self):
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    self.done = True
                for b in self.buttons:
                    b.get_event(event)
                        
        def run(self):
            while not self.done:
                self.screen.fill((255,255,255))
                self.event_loop()
                for b in self.buttons:
                    b.update()
                    b.render(self.screen)
                pg.display.update()
                self.Clock.tick(60)
                
        def terminate(self):
            self.done = True


    app = Control()
    app.run()
    pg.quit()
