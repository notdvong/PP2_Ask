import pygame
import sys
import json
import os
from config import *
from db import init_db, save_result, get_top_10, get_personal_best
from game import run_game



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Database Snake")
font_title = pygame.font.SysFont("Verdana", 40, bold=True)
font_norm = pygame.font.SysFont("Verdana", 20)

init_db()

def load_settings():
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w') as f:
            json.dump(DEFAULT_SETTINGS, f)
        return DEFAULT_SETTINGS
    with open('settings.json', 'r') as f:
        return json.load(f)

def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

settings = load_settings()

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.is_hovered = False

    def draw(self, surface):
        color = (100, 100, 100) if self.is_hovered else (50, 50, 50)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        text_surf = font_norm.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered

def draw_text_center(text, font, color, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH//2, y))
    screen.blit(surf, rect)

def main_menu():
    btn_play = Button(200, 150, 200, 40, "Play")
    btn_board = Button(200, 210, 200, 40, "Leaderboard")
    btn_settings = Button(200, 270, 200, 40, "Settings")
    btn_quit = Button(200, 330, 200, 40, "Quit")

    username = ""
    typing = False

    while True:
        screen.fill(BLACK)
        draw_text_center("SNAKE", font_title, GREEN, 50)
        
        input_rect = pygame.Rect(200, 100, 200, 30)
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        screen.blit(font_norm.render(username + ("|" if typing else ""), True, WHITE), (205, 102))

        pos = pygame.mouse.get_pos()
        for btn in [btn_play, btn_board, btn_settings, btn_quit]:
            btn.check_hover(pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or btn_quit.is_clicked(event):
                pygame.quit(); sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                typing = input_rect.collidepoint(event.pos)
                
            if event.type == pygame.KEYDOWN and typing:
                if event.key == pygame.K_BACKSPACE: username = username[:-1]
                elif len(username) < 15 and event.unicode.isalnum(): username += event.unicode
                
            if btn_play.is_clicked(event) and username: return "PLAY", username
            if btn_board.is_clicked(event): return "LEADERBOARD", username
            if btn_settings.is_clicked(event): return "SETTINGS", username

        pygame.display.flip()

def leaderboard_screen():
    btn_back = Button(200, 340, 200, 40, "Back")
    scores = get_top_10()

    while True:
        screen.fill(BLACK)
        draw_text_center("TOP 10", font_title, YELLOW, 30)
        
        y = 80
        for i, (name, score, lvl, date) in enumerate(scores):
            txt = f"{i+1}. {name} - Score: {score} (Lvl {lvl})"
            screen.blit(font_norm.render(txt, True, WHITE), (100, y))
            y += 25

        btn_back.check_hover(pygame.mouse.get_pos())
        btn_back.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if btn_back.is_clicked(event): return

        pygame.display.flip()

def settings_screen():
    global settings
    btn_color = Button(200, 100, 200, 40, "Change Color")
    btn_grid = Button(200, 160, 200, 40, f"Grid: {'ON' if settings['grid_overlay'] else 'OFF'}")
    btn_sound = Button(200, 220, 200, 40, f"Sound: {'ON' if settings['sound'] else 'OFF'}")
    btn_back = Button(200, 300, 200, 40, "Save & Back")

    colors = [[0, 255, 0], [255, 0, 0], [0, 0, 255], [255, 255, 0]]
    c_idx = 0

    while True:
        screen.fill(BLACK)
        draw_text_center("SETTINGS", font_title, WHITE, 40)
        
        pygame.draw.rect(screen, tuple(settings['snake_color']), (420, 105, 30, 30))

        pos = pygame.mouse.get_pos()
        for btn in [btn_color, btn_grid, btn_sound, btn_back]:
            btn.check_hover(pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if btn_color.is_clicked(event):
                c_idx = (c_idx + 1) % len(colors)
                settings['snake_color'] = colors[c_idx]
            if btn_grid.is_clicked(event):
                settings['grid_overlay'] = not settings['grid_overlay']
                btn_grid.text = f"Grid: {'ON' if settings['grid_overlay'] else 'OFF'}"
            if btn_sound.is_clicked(event):
                settings['sound'] = not settings['sound']
                btn_sound.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
            if btn_back.is_clicked(event):
                save_settings(settings)
                return

        pygame.display.flip()

def game_over_screen(stats, pb):
    btn_retry = Button(200, 250, 200, 40, "Retry")
    btn_menu = Button(200, 310, 200, 40, "Main Menu")

    while True:
        screen.fill(BLACK)
        draw_text_center("GAME OVER", font_title, RED, 80)
        draw_text_center(f"Final Score: {stats['score']}", font_norm, WHITE, 140)
        draw_text_center(f"Level Reached: {stats['level']}", font_norm, WHITE, 170)
        draw_text_center(f"Personal Best: {pb}", font_norm, YELLOW, 200)

        pos = pygame.mouse.get_pos()
        for btn in [btn_retry, btn_menu]:
            btn.check_hover(pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if btn_retry.is_clicked(event): return "PLAY"
            if btn_menu.is_clicked(event): return "MENU"

        pygame.display.flip()

state = "MENU"
current_user = ""

while True:
    if state == "MENU":
        state, current_user = main_menu()
    elif state == "PLAY":
        pb = get_personal_best(current_user)
        stats = run_game(screen, settings, current_user, pb)
        if stats is None: break
        save_result(current_user, stats['score'], stats['level'])
        new_pb = get_personal_best(current_user)
        state = game_over_screen(stats, new_pb)
    elif state == "LEADERBOARD":
        leaderboard_screen()
        state = "MENU"
    elif state == "SETTINGS":
        settings_screen()
        state = "MENU"

pygame.quit()
sys.exit()