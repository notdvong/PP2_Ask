import pygame
import random
import sys
from config import *

def run_game(screen, settings, username, personal_best):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 20)
    
    snake_pos = [[100, 60], [80, 60], [60, 60]]
    direction = 'RIGHT'
    change_to = direction
    
    score = 0
    level = 1
    base_fps = 10
    
    # Food System
    food_pos = [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
    food_spawn_time = pygame.time.get_ticks()
    poison_pos = None
    
    # Power-up System
    powerup_pos = None
    powerup_type = None
    powerup_spawn_time = 0
    active_powerup = None
    powerup_timer = 0
    shield_active = False
    
    # Obstacles
    obstacles = []

    def generate_safe_pos():
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            pos = [x, y]
            if pos not in snake_pos and pos not in obstacles:
                return pos

    def spawn_obstacles():
        obstacles.clear()
        if level >= 3:
            for _ in range(level * 2):
                pos = generate_safe_pos()
                if pos[0] > 200 or pos[1] > 100: 
                    obstacles.append(pos)

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN': change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP': change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT': change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT': change_to = 'RIGHT'

        direction = change_to
        head = list(snake_pos[0])
        
        if direction == 'UP': head[1] -= BLOCK_SIZE
        elif direction == 'DOWN': head[1] += BLOCK_SIZE
        elif direction == 'LEFT': head[0] -= BLOCK_SIZE
        elif direction == 'RIGHT': head[0] += BLOCK_SIZE

        snake_pos.insert(0, head)

        if head == food_pos:
            weight = random.choice([1, 1, 1, 3, 5])
            score += weight
            food_pos = generate_safe_pos()
            food_spawn_time = current_time
            if score // 5 >= level:
                level += 1
                spawn_obstacles()
        else:
            snake_pos.pop()

        if poison_pos and head == poison_pos:
            if len(snake_pos) > 2:
                snake_pos.pop()
                snake_pos.pop()
                poison_pos = None
            else:
                running = False 
                
        if powerup_pos and head == powerup_pos:
            active_powerup = powerup_type
            if active_powerup in ["Speed", "Slow"]:
                powerup_timer = current_time
            elif active_powerup == "Shield":
                shield_active = True
            powerup_pos = None

        if active_powerup in ["Speed", "Slow"] and current_time - powerup_timer > 5000:
            active_powerup = None

        if current_time - food_spawn_time > 10000:
            food_pos = generate_safe_pos()
            food_spawn_time = current_time

        if not poison_pos and random.random() < 0.01:
            poison_pos = generate_safe_pos()
        elif poison_pos and random.random() < 0.005:
            poison_pos = None

        if not powerup_pos and random.random() < 0.005:
            powerup_pos = generate_safe_pos()
            powerup_type = random.choice(["Speed", "Slow", "Shield"])
            powerup_spawn_time = current_time
        elif powerup_pos and current_time - powerup_spawn_time > 8000:
            powerup_pos = None

        collided = False
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT: collided = True
        if head in snake_pos[1:]: collided = True
        if head in obstacles: collided = True

        if collided:
            if shield_active:
                shield_active = False
                active_powerup = None
                snake_pos.pop(0)
                direction = 'RIGHT' 
            else:
                running = False

        screen.fill(BLACK)
        
        if settings.get("grid_overlay"):
            for x in range(0, WIDTH, BLOCK_SIZE):
                pygame.draw.line(screen, (30,30,30), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.line(screen, (30,30,30), (0, y), (WIDTH, y))

        for obs in obstacles:
            pygame.draw.rect(screen, GRAY, pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        if poison_pos:
            pygame.draw.rect(screen, DARK_RED, pygame.Rect(poison_pos[0], poison_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        if powerup_pos:
            color = YELLOW if powerup_type == "Speed" else CYAN if powerup_type == "Slow" else BLUE
            pygame.draw.rect(screen, color, pygame.Rect(powerup_pos[0], powerup_pos[1], BLOCK_SIZE, BLOCK_SIZE))

        snake_color = tuple(settings.get("snake_color", [0, 255, 0]))
        for block in snake_pos:
            pygame.draw.rect(screen, snake_color, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

        texts = [f"Score: {score}", f"Level: {level}", f"PB: {personal_best}"]
        if active_powerup: texts.append(f"[{active_powerup}]")
        
        for i, text in enumerate(texts):
            rendered = font.render(text, True, WHITE)
            screen.blit(rendered, (10, 10 + (i * 25)))

        pygame.display.update()

        fps = base_fps + (level * 2)
        if active_powerup == "Speed": fps += 10
        elif active_powerup == "Slow": fps = max(5, fps - 10)
        clock.tick(fps)

    return {"score": score, "level": level}