

import pygame as pg
import os


class Font:
    '''simulating tools'''
    path = 'resources/fonts'
    @staticmethod
    def load(filename, size):
        p = os.path.join(Font.path, filename+'.ttf')
        return pg.font.Font(os.path.abspath(p), size)
        
class Button:
    def __init__(self, text='', width=100, height=10, fontsize=15, font=None, 
        fg=(0,0,0), bg=(255,255,255), hover=(155,155,155), command=None, border=False):
        self.font = font
        self.text_color = fg
        self.label, self.label_rect = self.render_font(text, self.font, fontsize)
        self.bg_color = bg
        self.color = self.bg_color
        self.hover_bg_color = hover
        self.callback = command
        self.border = border
        self.image = pg.Surface([width,height]).convert()
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()
        self.label_rect.center = self.rect.center
        self.is_hover = False
        
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
        screen.blit(self.label, self.label_rect)
        
    def mouse_collision(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.is_hover = True
        else:
            self.is_hover = False
            
        if self.is_hover:
            self.color = self.hover_bg_color
        else:
            self.color = self.bg_color
            
    def update(self):
        self.label_rect.center = self.rect.center
        self.mouse_collision()
            
    def get_event(self, event):
        if self.is_hover:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.callback()

if __name__ == "__main__":

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
            
            self.btn = Button(text='Button1', width=100, height=20, font='impact',
                fg=(0,0,0), bg=(155,155,155), hover=(255,255,255), command=callback)
            self.btn.rect.center = (200,100)
            self.btn2 = Button(text='Button2', width=100, height=20, font='impact',
                fg=(0,0,0), bg=(155,155,155), hover=(255,255,255), command=callback2)
            self.btn2.rect.center = (200,150)
            self.quit_btn = Button(text='Quit', width=100, height=20, font='impact',
                fg=(255,0,0), bg=(155,155,155), hover=(255,255,255), command=self.terminate)
            self.quit_btn.rect.center = (200,200)
            self.buttons = [self.btn, self.btn2, self.quit_btn]
            
        def event_loop(self):
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    self.done = True
                for b in self.buttons:
                    b.get_event(event)
                        
        def run(self):
            while not self.done:
                self.screen.fill(0)
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

