import pygame
import sys
from clock import MickeyClock

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3.1 Mickey's Clock")
clock_timer = pygame.time.Clock()
mickey_clock = MickeyClock((WIDTH // 2, HEIGHT // 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    
    mickey_clock.draw(screen)

    pygame.display.flip()
    clock_timer.tick(60)

# Clean exit
pygame.quit()
sys.exit()