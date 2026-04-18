import pygame
import sys
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3.3 Moving Ball Game")
clock = pygame.time.Clock()

my_ball = Ball(WIDTH // 2, HEIGHT // 2, 25, RED)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_ball.move("UP", WIDTH, HEIGHT)
            elif event.key == pygame.K_DOWN:
                my_ball.move("DOWN", WIDTH, HEIGHT)
            elif event.key == pygame.K_LEFT:
                my_ball.move("LEFT", WIDTH, HEIGHT)
            elif event.key == pygame.K_RIGHT:
                my_ball.move("RIGHT", WIDTH, HEIGHT)

    screen.fill(WHITE) 
    my_ball.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()