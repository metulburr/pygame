
import pygame as pg
import os
import weakref
        
class Entry:
    instances = []
    def __init__(self, text='', width=100, height=10, fontsize=15, font=None, 
        fg=(0,0,0), deselect=(255,255,255), select=(155,155,155), bg=(255,255,255), border_width=5, border=False):
        
        Entry.instances.append(self)
        self.font = font
        self.text_color = fg
        self.label, self.label_rect = self.render_font(text, self.font, fontsize)
        self.bg_color = deselect
        self.background_color = bg
        self.color = self.bg_color
        self.hover_bg_color = select
        self.border_width = border_width
        self.border = border
        self.image = pg.Surface([width,height]).convert()
        self.image.fill(self.bg_color)
        self.background = pg.Surface([width-self.border_width,height-self.border_width]).convert()
        self.background.fill(self.background_color)
        self.background_rect = self.background.get_rect()
        self.rect = self.image.get_rect()
        self.label_rect.center = self.rect.center
        self.background_rect.center = self.rect.center
        self.focus = False
        
    def render_font(self, text, filename, size):
        if not filename:
            f = pg.font.SysFont('Arial', size)
        else:
            f = Font.load(self.font, size)
        font = f.render(text, 1, self.text_color)
        rect = font.get_rect()
        return (font, rect)
        
    def render(self, screen):
        pg.draw.rect(screen, self.color, self.rect, self.border)
        pg.draw.rect(screen, self.background_color, self.background_rect, False)
        screen.blit(self.label, self.label_rect)
        
    def mouse_collision(self):
        if self.focus:
            self.color = self.hover_bg_color
        else:
            self.color = self.bg_color
            
    def update(self):
        self.label_rect.center = self.rect.center
        self.background_rect.center = self.rect.center
        self.mouse_collision()
            
    def get_event(self, event):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for obj in Entry.instances[:]: #reset all other Entry focus to False
                    obj.focus = False
                self.focus = not self.focus
            

if __name__ == "__main__":
    
    class Font:
        '''simulating tools'''
        path = 'resources/fonts'
        @staticmethod
        def load(filename, size):
            p = os.path.join(Font.path, filename+'.ttf')
            return pg.font.Font(os.path.abspath(p), size)
        
    class Control:
        def __init__(self):
            pg.init()
            self.screen = pg.display.set_mode((800,600))
            self.screen_rect = self.screen.get_rect()
            self.Clock = pg.time.Clock()
            self.done = False
            
            self.e = Entry(text='default text 1', width=300, height=30, fontsize=20,
                fg=(0,0,0), deselect=(255,255,255), select=(0,0,0))
            self.e.rect.center = (200,100)
            self.e2 = Entry(text='default text 2', width=300, height=30, fontsize=20,
                fg=(0,0,0), deselect=(255,255,255), select=(0,0,0))
            self.e2.rect.center = (200,150)
            self.e3 = Entry(text='default text 3', width=300, height=30, fontsize=20,
                fg=(0,0,0), deselect=(255,255,255), select=(0,0,0))
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
                self.screen.fill((155,155,155))
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
