
import pygame as pg

class Player:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.width = 50
        self.height = 75
        self.image = pg.Surface([self.width, self.height])
        self.image.fill((255,255,255))
        starting_loc = (0, screen_rect.height - self.height)
        self.rect = self.image.get_rect(bottomleft=starting_loc)
        self.speed = 5
        self.grav = .5

        self.jumping = False
        self.y_vel = 0
        
    def update(self):
        self.rect.clamp_ip(self.screen_rect)
        self.jump_update()
        
    def render(self, screen):
        screen.blit(self.image, self.rect)
        
    def move(self, x, y):
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed
                
    def jump_update(self):
        if self.jumping:
            self.y_vel += self.grav
            self.rect.y += self.y_vel
            if self.is_touching_ground():
                self.jumping = False
                
    def is_touching_ground(self):
        return self.rect.y >= self.screen_rect.height - self.height
            
        
    def jump(self):
        if not self.jumping:
            self.y_vel = -12
            self.jumping = True
