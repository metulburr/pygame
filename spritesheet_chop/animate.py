
import os
import pygame as pg

class Bomb:
    def __init__(self,rect):
        self.rect = pg.Rect(rect)
        self.image = None
        self.spritesheet = pg.image.load("explosion.png").convert_alpha()
        self.frame  = 0
        self.frames = [] #all frames off the sprite sheet
        self.timer = 0.0 #timer for animation
        self.fps   = 30.0 #fps of animation
        self.get_images(8,6,3) #rip images from the sprite sheet
        self.done = False
        
    def get_images(self, num_img_row, num_img_col, empty_frames=0):
        for col in range(num_img_col):
            for row in range(num_img_row):
                loc = ((self.rect.width * row, self.rect.height * col), self.rect.size)
                self.frames.append(self.spritesheet.subsurface(loc))
        if empty_frames:
            for empty_frame in range(empty_frames):
                self.frames.pop()
        self.make_image()
        
    def make_image(self):
        if pg.time.get_ticks()-self.timer > 1000/self.fps:
            try:
                self.frame += 1
                self.image = self.frames[self.frame]
                self.timer = pg.time.get_ticks()
            except IndexError:
                self.done = True
        if not self.image:
            self.image = self.frames[self.frame]

            
    def update(self, surf):
        self.make_image()
        surf.blit(self.image, self.rect)

class Control:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pg.display.set_mode((256,256))
        pg.display.set_caption('Press Space Bar')
        pg.init()
        self.Clock = pg.time.Clock()
        self.done = False
        self.bombs = []
        
    def event_loop(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.bombs.append(Bomb((0,0,256,256)))
                    
    def update(self):
        while not self.done:
            self.event_loop()
            self.screen.fill(0)
            for bomb in self.bombs[:]:
                bomb.update(self.screen)
                if bomb.done:
                    self.bombs.remove(bomb)
            pg.display.update()
            self.Clock.tick(60)

if __name__ == "__main__":
    app = Control()
    app.update()
    pg.quit()
