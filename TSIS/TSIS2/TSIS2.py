import pygame
import sys
import datetime

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Pygame Paint")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [BLACK, RED, GREEN, BLUE, YELLOW]
color_index = 0
current_color = COLORS[color_index]


font = pygame.font.SysFont("Verdana", 14)
text_tool_font = pygame.font.SysFont("Verdana", 24)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

brush_sizes = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10} # Small, Medium, Large
current_size = 5

mode = 'pencil' 
drawing = False
start_pos = (0, 0)
last_pos = (0, 0)

typing = False
text_input = ""
text_pos = (0, 0)

clock = pygame.time.Clock()

def flood_fill(surface, pos, target_color, fill_color):
    """
    Fills a closed region using surface.get_at() and surface.set_at().
    Uses an iterative approach (stack) to avoid recursion limits.
    """
    if target_color == fill_color:
        return
    
    stack = [pos]
    while stack:
        x, y = stack.pop()
        
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            continue
            
        if surface.get_at((x, y)) == target_color:
            surface.set_at((x, y), fill_color)
            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"canvas_{timestamp}.png"
                pygame.image.save(canvas, filename)
                print(f"Saved: {filename}")
                continue
            

            if typing:
                if event.key == pygame.K_RETURN:
                    rendered_text = text_tool_font.render(text_input, True, current_color)
                    canvas.blit(rendered_text, text_pos)
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode
                continue


            if event.key == pygame.K_p: mode = 'pencil'
            elif event.key == pygame.K_l: mode = 'line'
            elif event.key == pygame.K_r: mode = 'rect'
            elif event.key == pygame.K_c: mode = 'circle'
            elif event.key == pygame.K_e: mode = 'eraser'
            elif event.key == pygame.K_f: mode = 'fill'
            elif event.key == pygame.K_t: mode = 'text'
            
            elif event.key == pygame.K_s: mode = 'square'
            elif event.key == pygame.K_y: mode = 'right_tri'
            elif event.key == pygame.K_u: mode = 'eq_tri'
            elif event.key == pygame.K_i: mode = 'rhombus'
            
            elif event.key in brush_sizes:
                current_size = brush_sizes[event.key]
                
            elif event.key == pygame.K_UP:
                color_index = (color_index + 1) % len(COLORS)
                current_color = COLORS[color_index]
            
            elif event.key == pygame.K_SPACE: canvas.fill(WHITE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                start_pos = event.pos
                last_pos = event.pos
                
                if mode == 'fill':
                    target_col = canvas.get_at(start_pos)
                    flood_fill(canvas, start_pos, target_col, current_color)
                elif mode == 'text':
                    typing = True
                    text_input = ""
                    text_pos = start_pos
                else:
                    drawing = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                end_pos = event.pos
                
                if mode == 'line':
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, current_size)
                
                elif mode == 'rect':
                    r_rect = pygame.Rect(start_pos[0], start_pos[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
                    r_rect.normalize() 
                    pygame.draw.rect(canvas, current_color, r_rect, current_size)
                
                elif mode == 'circle':
                    radius = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, current_size)
                
                elif mode == 'square':
                    side = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    dx = 1 if end_pos[0] > start_pos[0] else -1
                    dy = 1 if end_pos[1] > start_pos[1] else -1
                    s_rect = pygame.Rect(start_pos[0], start_pos[1], side * dx, side * dy)
                    s_rect.normalize()
                    pygame.draw.rect(canvas, current_color, s_rect, current_size)    
                
                elif mode == 'right_tri':
                    points = [start_pos, (start_pos[0], end_pos[1]), end_pos]
                    pygame.draw.polygon(canvas, current_color, points, current_size)
                
                elif mode == 'eq_tri':
                    mid_x = start_pos[0] + (end_pos[0] - start_pos[0]) / 2
                    points = [(mid_x, start_pos[1]), (start_pos[0], end_pos[1]), (end_pos[0], end_pos[1])]
                    pygame.draw.polygon(canvas, current_color, points, current_size)
                
                elif mode == 'rhombus':
                    mid_x = start_pos[0] + (end_pos[0] - start_pos[0]) / 2
                    mid_y = start_pos[1] + (end_pos[1] - start_pos[1]) / 2
                    points = [(mid_x, start_pos[1]), (end_pos[0], mid_y), (mid_x, end_pos[1]), (start_pos[0], mid_y)]
                    pygame.draw.polygon(canvas, current_color, points, current_size)

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if mode == 'pencil':
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, current_size)
                    last_pos = event.pos 
                elif mode == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, current_size * 2) 

    screen.blit(canvas, (0, 0))

    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        if mode == 'line':
            pygame.draw.line(screen, current_color, start_pos, mouse_pos, current_size)
        elif mode == 'rect':
            t_rect = pygame.Rect(start_pos[0], start_pos[1], mouse_pos[0] - start_pos[0], mouse_pos[1] - start_pos[1])
            t_rect.normalize()
            pygame.draw.rect(screen, current_color, t_rect, current_size)
        elif mode == 'circle':
            radius = max(abs(mouse_pos[0] - start_pos[0]), abs(mouse_pos[1] - start_pos[1]))
            pygame.draw.circle(screen, current_color, start_pos, radius, current_size)
        elif mode == 'square':
            side = max(abs(mouse_pos[0] - start_pos[0]), abs(mouse_pos[1] - start_pos[1]))
            dx = 1 if mouse_pos[0] > start_pos[0] else -1
            dy = 1 if mouse_pos[1] > start_pos[1] else -1
            s_rect = pygame.Rect(start_pos[0], start_pos[1], side * dx, side * dy)
            s_rect.normalize()
            pygame.draw.rect(screen, current_color, s_rect, current_size)


    if typing:
        preview_text = text_tool_font.render(text_input + "|", True, current_color)
        screen.blit(preview_text, text_pos)

    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 60))
    pygame.draw.line(screen, BLACK, (0, 60), (WIDTH, 60), 2)
    
    controls1 = "TOOLS: [P]encil, [L]ine, [R]ect, [C]ircle, [E]raser, [F]ill, [T]ext | [Ctrl+S] Save"
    controls2 = "SHAPES: [S]quare, [Y]Right-Tri, [U]Eq-Tri, [I]Rhombus | COLORS: [UP-Arrow] Cycle"
    status = f"MODE: {mode.upper()} | SIZE: {current_size}px (Keys 1,2,3)"
    
    screen.blit(font.render(controls1, True, BLACK), (10, 5))
    screen.blit(font.render(controls2, True, BLACK), (10, 30))
    screen.blit(font.render(status, True, RED), (WIDTH - 300, 15))

    pygame.display.flip()
    clock.tick(120)