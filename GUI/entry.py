



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
        self.border_image = pg.Surface([width,height]).convert()
        self.image.fill(self.bg_color)
        self.border_image.fill(self.bg_color)
        self.rect = self.image.get_rect()
        self.border_rect = self.border_image.get_rect()
        self.border_rect.width += self.border_width
        self.border_rect.height += self.border_width
        self.focus = False
        
    def assign_kwargs(self, kwargs):
        self.bg_color = kwargs['bg']
        self.text_color = kwargs['font_color']
        self.font = kwargs['font']
        self.border_color_init = kwargs['border_color']
        self.border_width = kwargs['border_width']
        self.fontsize = kwargs['font_size']
        
    def render_font(self, text, filename, size):
        if not filename:
            f = pg.font.SysFont('Arial', size)
        else:
            f = Font.load(self.font, size)
        font = f.render(text, 1, self.text_color)
        rect = font.get_rect()
        return (font, rect)
        
    def render(self, screen):
        pg.draw.rect(screen, self.border_color, self.border_rect, False)
        pg.draw.rect(screen, self.color, self.rect, False)
        screen.blit(self.label, self.label_rect)
            
    def update(self):
        self.border_rect.center = self.rect.center
        self.label_rect.left = self.rect.left
        self.label_rect.centery = self.rect.centery
        if self.focus:
            self.border_color = self.border_color_init
        else:
            self.border_color = self.bg_color

        if self.label_rect.width > self.rect.width:
            self.label_rect.right= self.rect.right
            #self.label_rect.width = self.rect.width
            #self.label_rect.clip(self.rect)
            #self.label_rect.fit(self.rect)
            
        
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.focus:
                if event.unicode.isprintable():
                    self.text += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_DELETE:
                    self.text = ''
                self.label, self.label_rect = self.render_font(self.text, self.font, self.fontsize)
        elif self.rect.collidepoint(pg.mouse.get_pos()):
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for obj in Entry.instances: 
                    obj.focus = False
                self.focus = not self.focus

            

if __name__ == "__main__":
        
    class Font:
        '''simulating tools'''
        path = 'resources/fonts'
        @staticmethod
        def load(filename, size):
            p = os.path.join(Font.path, filename)
            return pg.font.Font(os.path.abspath(p), size)
        
    class Control:
        def __init__(self):
            pg.init()
            self.screen = pg.display.set_mode((800,600))
            self.screen_rect = self.screen.get_rect()
            self.Clock = pg.time.Clock()
            self.done = False
            
            self.entry_settings = {
                'font'         : 'impact.ttf',
                'font_color'   : (200,200,0),
                'bg'           : (255,255,255),
                'border_color' : (0,0,255),
                'border_width' : 5,
                'font_size'    : 15
            }
            
            self.e = Entry(text='default text', width=100, height=20, **self.entry_settings)
            self.e.rect.center = (200,100)
            self.e2 = Entry(text='default text', width=100, height=20, **self.entry_settings)
            self.e2.rect.center = (200,150)
            self.e3 = Entry(text='default text', width=100, height=20, **self.entry_settings)
            self.e3.rect.center = (200,200)
            self.entries = [self.e, self.e2, self.e3]
            
        def event_loop(self):
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    self.done = True
                for b in self.entries:
                    b.get_event(event)
                        
        def run(self):
            while not self.done:
                self.screen.fill((0,0,0))
                self.event_loop()
                for b in self.entries:
                    b.update()
                    b.render(self.screen)
                pg.display.update()
                self.Clock.tick(60)
                
        def terminate(self):
            self.done = True


    app = Control()
    app.run()
    pg.quit()
