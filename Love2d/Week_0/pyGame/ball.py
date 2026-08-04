import pygame, random

pygame.mixer.init()
hit1 = pygame.mixer.Sound('Love2d/Week_0/assets/hit1.wav')
hit2 = pygame.mixer.Sound('Love2d/Week_0/assets/hit2.wav')

volume = hit1.get_volume() * 0.3 
hit1.set_volume(volume)



class Ball:
    def __init__(self, x, y, r, m, screen_height):
        self.screen_h = screen_height
        self.x = x
        self.y = y
        self.r = r * m
        self.dx = random.choice([-100 * m, 100 * m])
        self.dy = random.randint(-50 * m, 50 * m)
        self.rect = pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)
    
    def update(self, dt):
        self.x = self.x + self.dx * dt
        self.y = self.y + self.dy * dt
        
        # wall bounce
        if self.y < 0:
            self.y += self.r / 3
            self.dy *= -1
            hit2.play()
        elif self.y + self.r > self.screen_h:
            self.dy *= -1
            self.y -= self.r / 3
            hit2.play()
        

        # update rect
        self.rect = pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)
    
    def render(self, surface):
        pygame.draw.circle(surface, 'white', (self.x, self.y), self.r)
        
    def bounce(self):
        if self.dx < 0:
            self.x += 5
        else:
            self.x -= 5
        self.dx *= -1.1
        self.dy *= random.uniform(0.9, 1.5)
        hit1.play()