import pygame
from paddle import Paddle
from ball import Ball

WIDTH = 1280
HEIGHT = 720    

multi = 3

PADDLE_SPEED = 200 * multi
PADDLE_WIDTH = 6 * multi
PADDLE_HEIGHT = 30 * multi

game_state = 'start'

dt = 0
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()


player_1 = Paddle(50,100, PADDLE_WIDTH, PADDLE_HEIGHT, 'white', HEIGHT)
player_2 = Paddle(WIDTH-PADDLE_WIDTH-50,100, PADDLE_WIDTH, PADDLE_HEIGHT, 'white', HEIGHT)
p1_score = 0
p2_score = 0
ball = Ball(WIDTH/2, HEIGHT/2, 5, multi, HEIGHT)

font = pygame.font.Font(None, 46)
info = font.render('Press ENTER to start', True, 'white')
info_rect = info.get_rect(center=(WIDTH//2, HEIGHT * 0.4))

running = True
while running:
    ### events ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if game_state == 'start':
                    game_state = 'play'
                else:
                    game_state = 'start'
                    ball = Ball(WIDTH/2, HEIGHT/2, 5, multi, HEIGHT)
                
    screen.fill((43,45,70))
    
    ### key input ###
    keys = pygame.key.get_pressed()
    # p1           
    if keys[pygame.K_w]:
        player_1.dy = -PADDLE_SPEED 
    elif keys[pygame.K_s]:
        player_1.dy =  PADDLE_SPEED
    else:
        player_1.dy = 0
    #p2
    if keys[pygame.K_UP]:
        player_2.dy = -PADDLE_SPEED
    elif keys[pygame.K_DOWN]:
        player_2.dy = PADDLE_SPEED
    else:
        player_2.dy = 0
    ### update ###
    player_1.update(dt)
    player_2.update(dt)
    score_surface = font.render(f'{p1_score} {" "*60} {p2_score}', True, 'white')
    score_rect = score_surface.get_rect(center=(WIDTH//2, HEIGHT * 0.1))
    screen.blit(score_surface, score_rect)
    
    if game_state == 'play':
        ball.update(dt)
    if game_state == 'start':
        screen.blit(info, info_rect)
        
    if ball.rect.colliderect(player_1.rect) or ball.rect.colliderect(player_2.rect):
        ball.bounce()
        

    ### render ###
    
    player_1.render(screen)
    player_2.render(screen)
    
    ball.render(screen)
    pygame.display.flip()
    ###
    dt = clock.tick(60) / 1000
    
pygame.quit()