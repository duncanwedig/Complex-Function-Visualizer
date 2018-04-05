import sys, pygame, time
from vector import Vector, vectortype
pygame.init()


class Planet(object):
    
    velocity = Vector([-20, 0], vectortype.XY)
    start_time = 0
    
    def __init__(self, location, radius, gravity_radius):
        self.position = location
        self.rect = pygame.Rect(location.xy(), (radius*2, radius*2))
        self.size = radius
        self.gravity_size = gravity_radius
        self.surface = pygame.image.load("planet.png").convert_alpha()
        self.gravity_image = pygame
        pass

    @classmethod
    def set_start_time(self, time):
        self.start_time = time

    def get_y(self):
        return self.position.y

    def get_x(self):
        return self.position.x

    def move(self, duration):
        self.position += self.velocity * duration / 1000
        self.rect.move_ip(self.position.x-self.rect.x, self.position.y - self.rect.y)
    
    def get_blit_data(self):
        return ((self.surface, self.rect))
    
    def update(self, screen, current_time):
        self.move(current_time-self.start_time)
        screen.blit(*self.get_blit_data())
    
    

