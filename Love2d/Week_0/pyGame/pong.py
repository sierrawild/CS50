import pygame
from Paddle import Paddle

WIDTH = 1280
HEIGHT = 720    

PADDLE_SPEED = 200
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 30

dt = 0
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()


player_1 = Paddle(50,100, PADDLE_WIDTH, PADDLE_HEIGHT, 'red', HEIGHT)

running = True
while running:
    ### events ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill("#292E2D")
    
    ### key input ###
    keys = pygame.key.get_pressed()            
    
    ### update ###
    
    ### render ###
    
    player_1.render(screen)
    
    pygame.display.flip()
    ###
    dt = clock.tick(60) / 1000
    
pygame.quit()