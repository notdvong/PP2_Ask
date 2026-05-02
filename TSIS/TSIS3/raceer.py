import pygame
import random
import time
import os

WIDTH, HEIGHT = 400, 600

def get_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stuff', filename)

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.original_image = pygame.image.load(get_path("Player.png")).convert_alpha()
        self.image = self.original_image.copy()
  
        color_map = {"Blue": (100, 100, 255), "Red": (255, 100, 100), "Green": (100, 255, 100)}
        tint = color_map.get(color_name, (255, 255, 255))
        self.image.fill(tint, special_flags=pygame.BLEND_MULT)
        
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 100))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_path("Enemy.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -50))
        
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(get_path("dollar.png")).convert_alpha()
        self.image = pygame.transform.scale(img, (40, 40))
        
        self.weight = random.choice([1, 1, 1, 5, 5, 10]) 
        if self.weight == 10:
             self.image.fill((200, 200, 255), special_flags=pygame.BLEND_MULT)
             
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -50))
        
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill((100, 100, 100)) 
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -50))
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT: self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 255)) # Cyan box
        self.type = random.choice(["Nitro", "Shield", "Repair"])
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -50))
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT: self.kill()

def run_game(screen, settings, username):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 20)
    
    bg_image = pygame.image.load(get_path("AnimatedStreet.png")).convert()
    bg_y = 0
    
    pygame.mixer.music.load(get_path('background.wav'))
    crash_sound = pygame.mixer.Sound(get_path('crash.wav'))
    
    if settings['sound']:
        pygame.mixer.music.play(-1)
    
    base_speed = 5 if settings['difficulty'] == "Normal" else 8
    speed = base_speed
    score = 0
    distance = 0
    coins_collected = 0
    
    active_powerup = None
    powerup_timer = 0
    shield_active = False

    player = Player(settings['car_color'])
    all_sprites = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, 1000)
    SPAWN_COIN = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_COIN, 2000)
    SPAWN_OBSTACLE = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_OBSTACLE, 3000)
    SPAWN_POWERUP = pygame.USEREVENT + 4
    pygame.time.set_timer(SPAWN_POWERUP, 10000)

    running = True
    while running:
        distance += (speed / 10) 
        current_speed = speed + (distance // 500) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return None
            
            if event.type == SPAWN_ENEMY:
                e = Enemy()
                enemies.add(e); all_sprites.add(e)
            if event.type == SPAWN_COIN:
                c = Coin()
                coins.add(c); all_sprites.add(c)
            if event.type == SPAWN_OBSTACLE:
                o = Obstacle()
                obstacles.add(o); all_sprites.add(o)
            if event.type == SPAWN_POWERUP:
                p = Powerup()
                powerups.add(p); all_sprites.add(p)

        if active_powerup and time.time() > powerup_timer:
            active_powerup = None 
            speed = base_speed
    
        for c in pygame.sprite.spritecollide(player, coins, True):
            coins_collected += c.weight
            score += c.weight * 10
            base_speed += 0.1 

        hit_powerup = pygame.sprite.spritecollideany(player, powerups)
        if hit_powerup:
            hit_powerup.kill()
            active_powerup = hit_powerup.type
            if active_powerup == "Nitro":
                speed = base_speed * 2
                powerup_timer = time.time() + 4
            elif active_powerup == "Shield":
                shield_active = True
                powerup_timer = time.time() + 999 
            elif active_powerup == "Repair":
                for e in enemies: e.kill()
                for o in obstacles: o.kill()
                active_powerup = None 

        if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, obstacles):
            if shield_active:
                shield_active = False
                active_powerup = None
                for item in pygame.sprite.spritecollide(player, enemies, True): pass
                for item in pygame.sprite.spritecollide(player, obstacles, True): pass
            else:
                if settings['sound']:
                    pygame.mixer.music.stop()
                    crash_sound.play()
                    pygame.time.wait(1000) 
                running = False 




        bg_y += current_speed
        if bg_y >= HEIGHT:
            bg_y = 0
        screen.blit(bg_image, (0, bg_y))
        screen.blit(bg_image, (0, bg_y - HEIGHT))
        
        player.move()
        for sprite in all_sprites:
            if sprite != player:
                sprite.move(current_speed)
            screen.blit(sprite.image, sprite.rect)

        def draw_ui_text(text, color, pos):
            screen.blit(font.render(text, True, (0,0,0)), (pos[0]+2, pos[1]+2))
            screen.blit(font.render(text, True, color), pos)

        draw_ui_text(f"Score: {int(score + distance)}", (255, 255, 255), (10, 10))
        draw_ui_text(f"Dist: {int(distance)}m", (255, 255, 255), (10, 35))
        draw_ui_text(f"Coins: {coins_collected}", (255, 215, 0), (WIDTH - 120, 10))
        
        if active_powerup:
            draw_ui_text(f"[{active_powerup}]", (0, 255, 255), (WIDTH//2 - 40, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    return {"name": username, "score": int(score + distance), "distance": int(distance), "coins": coins_collected}