import pygame

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = 20

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move(self, direction, screen_width, screen_height):
        new_x, new_y = self.x, self.y

        if direction == "UP":
            new_y -= self.velocity
        elif direction == "DOWN":
            new_y += self.velocity
        elif direction == "LEFT":
            new_x -= self.velocity
        elif direction == "RIGHT":
            new_x += self.velocity

        if (self.radius <= new_x <= screen_width - self.radius and 
            self.radius <= new_y <= screen_height - self.radius):
            self.x = new_x
            self.y = new_y