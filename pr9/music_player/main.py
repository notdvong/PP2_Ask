import pygame
import sys
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 500, 300
BLACK = (20, 20, 20)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3.2 Music Player")
font = pygame.font.SysFont("Arial", 24)

player = MusicPlayer("music")

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

running = True
while running:
    screen.fill(BLACK)
    
    draw_text("Music Player Controls:", 20, 20, GREEN)
    draw_text("[P] Play  [S] Stop  [N] Next  [B] Prev  [Q] Quit", 20, 60)
    
    status = "Playing" if player.is_playing else "Stopped"
    draw_text(f"Status: {status}", 20, 120)
    draw_text(f"Track: {player.get_current_track_name()}", 20, 160, (100, 200, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play_track()
            elif event.key == pygame.K_s:
                player.stop_track()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.prev_track()
            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()
sys.exit()