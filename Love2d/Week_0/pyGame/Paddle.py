import pygame

class Paddle:
    def __init__ (self,x,y, width, heigh, color, screen_heigh):
        self.x = x
        self.y = y
        self.width = width
        self.heigh = heigh
        self.dy = 0
        self.screen_h = screen_heigh
        self.color = color
        
    def update(self, dt):
        if self.dy < 0:
            self.y = max(0, self.y + self.dy * dt)
        else:
            self.y = min(self.screen_h - self.heigh, self.y + self.dy * dt)
            
    def render(self, surface):
        self.rect = (self.x, self.y, self.width, self.heigh)
        pygame.draw.rect(surface, self.color, self.rect)