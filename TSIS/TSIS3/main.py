import pygame
import sys
from persistence import load_settings, save_settings, load_leaderboard, save_leaderboard
from ui import Button, TextInput
from raceer import run_game

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Racer")
font_title = pygame.font.SysFont("Verdana", 40, bold=True)
font_norm = pygame.font.SysFont("Verdana", 20)

settings = load_settings()

def draw_text_center(text, font, color, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH//2, y))
    screen.blit(surf, rect)

def main_menu():
    btn_play = Button(100, 200, 200, 50, "Play", (0, 150, 0), (0, 200, 0))
    btn_board = Button(100, 270, 200, 50, "Leaderboard", (0, 0, 150), (0, 0, 200))
    btn_settings = Button(100, 340, 200, 50, "Settings", (150, 100, 0), (200, 150, 0))
    btn_quit = Button(100, 410, 200, 50, "Quit", (150, 0, 0), (200, 0, 0))

    while True:
        screen.fill((30, 30, 30))
        draw_text_center("RACER", font_title, (255, 255, 255), 100)

        mouse_pos = pygame.mouse.get_pos()
        for btn in [btn_play, btn_board, btn_settings, btn_quit]:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or btn_quit.is_clicked(event):
                pygame.quit(); sys.exit()
            if btn_play.is_clicked(event):
                return "NAME_ENTRY"
            if btn_board.is_clicked(event):
                return "LEADERBOARD"
            if btn_settings.is_clicked(event):
                return "SETTINGS"

        pygame.display.flip()

def name_entry_screen():
    input_box = TextInput(100, 250, 200, 40)
    btn_start = Button(100, 320, 200, 50, "Start Race", (0, 150, 0), (0, 200, 0))

    while True:
        screen.fill((30, 30, 30))
        draw_text_center("Enter Username:", font_norm, (255, 255, 255), 200)
        
        input_box.draw(screen)
        btn_start.check_hover(pygame.mouse.get_pos())
        btn_start.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            input_box.handle_event(event)
            if btn_start.is_clicked(event) and len(input_box.text) > 0:
                return input_box.text

        pygame.display.flip()

def game_over_screen(stats):
    save_leaderboard(stats)
    btn_retry = Button(100, 350, 200, 50, "Retry", (0, 150, 0), (0, 200, 0))
    btn_menu = Button(100, 420, 200, 50, "Main Menu", (0, 0, 150), (0, 0, 200))

    while True:
        screen.fill((50, 0, 0))
        draw_text_center("GAME OVER", font_title, (255, 255, 255), 100)
        draw_text_center(f"Score: {stats['score']}", font_norm, (255, 255, 255), 180)
        draw_text_center(f"Distance: {stats['distance']}m", font_norm, (255, 255, 255), 220)
        draw_text_center(f"Coins: {stats['coins']}", font_norm, (255, 215, 0), 260)

        mouse_pos = pygame.mouse.get_pos()
        for btn in [btn_retry, btn_menu]:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_retry.is_clicked(event): return "PLAY"
            if btn_menu.is_clicked(event): return "MENU"

        pygame.display.flip()

def leaderboard_screen():
    btn_back = Button(100, 500, 200, 50, "Back", (100, 100, 100), (150, 150, 150))
    board = load_leaderboard()

    while True:
        screen.fill((30, 30, 30))
        draw_text_center("TOP 10 SCORES", font_title, (255, 215, 0), 50)
        
        y = 120
        for i, entry in enumerate(board):
            text = f"{i+1}. {entry['name']} - {entry['score']} ({entry['distance']}m)"
            draw_text_center(text, font_norm, (255, 255, 255), y)
            y += 35

        btn_back.check_hover(pygame.mouse.get_pos())
        btn_back.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if btn_back.is_clicked(event): return

        pygame.display.flip()

def settings_screen():
    global settings
    btn_color = Button(100, 200, 200, 50, f"Car: {settings['car_color']}", (100, 100, 100), (150, 150, 150))
    btn_diff = Button(100, 270, 200, 50, f"Diff: {settings['difficulty']}", (100, 100, 100), (150, 150, 150))
    btn_back = Button(100, 400, 200, 50, "Save & Back", (0, 150, 0), (0, 200, 0))
    
    colors = ["Blue", "Red", "Green"]
    diffs = ["Normal", "Hard"]

    while True:
        screen.fill((30, 30, 30))
        draw_text_center("SETTINGS", font_title, (255, 255, 255), 100)

        mouse_pos = pygame.mouse.get_pos()
        for btn in [btn_color, btn_diff, btn_back]:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if btn_color.is_clicked(event):
                idx = (colors.index(settings['car_color']) + 1) % len(colors)
                settings['car_color'] = colors[idx]
                btn_color.text = f"Car: {settings['car_color']}"
            if btn_diff.is_clicked(event):
                idx = (diffs.index(settings['difficulty']) + 1) % len(diffs)
                settings['difficulty'] = diffs[idx]
                btn_diff.text = f"Diff: {settings['difficulty']}"
            if btn_back.is_clicked(event):
                save_settings(settings)
                return

        pygame.display.flip()



state = "MENU"
current_user = ""

while True:
    if state == "MENU":
        state = main_menu()
    elif state == "NAME_ENTRY":
        current_user = name_entry_screen()
        state = "PLAY"
    elif state == "PLAY":
        stats = run_game(screen, settings, current_user)
        if stats is None: break 
        state = "GAME_OVER"
        final_stats = stats
    elif state == "GAME_OVER":
        action = game_over_screen(final_stats)
        state = "PLAY" if action == "PLAY" else "MENU"
    elif state == "LEADERBOARD":
        leaderboard_screen()
        state = "MENU"
    elif state == "SETTINGS":
        settings_screen()
        state = "MENU"

pygame.quit()
sys.exit()