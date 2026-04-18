import pygame
import datetime

class MickeyClock:
    def __init__(self, screen_center):
        self.center = screen_center
        
        self.bg_clock = pygame.image.load("images/clock.png").convert_alpha()
        self.mickey = pygame.image.load("images/mickey.png").convert_alpha()
        left_img = pygame.image.load("images/left_hand.png").convert_alpha()
        right_img = pygame.image.load("images/right_hand.png").convert_alpha()

        SCALE = 0.85 
        
        l_size = (int(left_img.get_width() * SCALE), int(left_img.get_height() * SCALE))
        r_size = (int(right_img.get_width() * SCALE), int(right_img.get_height() * SCALE))
        
        self.left_hand = pygame.transform.scale(left_img, l_size)
        self.right_hand = pygame.transform.scale(right_img, r_size)

    def draw(self, surface):
        surface.blit(self.bg_clock, self.bg_clock.get_rect(center=self.center))

        surface.blit(self.mickey, self.mickey.get_rect(center=self.center))

        now = datetime.datetime.now()

        sec_angle = 0 - (now.second * 6)
        min_angle = 0 - (now.minute * 6)

        s_rotated = pygame.transform.rotate(self.left_hand, sec_angle)
        s_rect = s_rotated.get_rect(center=self.center)
        surface.blit(s_rotated, s_rect)

        m_rotated = pygame.transform.rotate(self.right_hand, min_angle)
        m_rect = m_rotated.get_rect(center=self.center)
        surface.blit(m_rotated, m_rect)