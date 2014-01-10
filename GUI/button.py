

import pygame as pg
        
class Button:
    def __init__(self, text='', width=100, height=10, 
        fg=(0,0,0), bg=(255,255,255), hover=(155,155,155), command=None, border=False):
            
        self.text_color = fg
        self.label, self.label_rect = self.font(text, 'arial', 15)
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
        
    def font(self, text, filename, size):
        f = pg.font.SysFont(filename, size)
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
            
            self.btn = Button(text='Button1', width=100, height=20, 
                fg=(0,0,0), bg=(155,155,155), hover=(255,255,255), command=callback)
            self.btn.rect.center = (200,100)
            self.btn2 = Button(text='Button2', width=100, height=20, 
                fg=(0,0,0), bg=(155,155,155), hover=(255,255,255), command=callback2)
            self.btn2.rect.center = (200,200)
            self.buttons = [self.btn, self.btn2]
            
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


    app = Control()
    app.run()
    pg.quit()

