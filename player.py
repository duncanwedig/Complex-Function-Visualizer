import pygame, extramath, math
from vector import Vector, vectortype

class Player(object):

    size = 75
    start_time = 0
    image = "ball.png"
    acceleration = 40
    collision_threshold = .5

    def __init__(self, position):
        self.position = position
        self.velocity = Vector((-20, 0), vectortype.XY)
        self.surface = pygame.image.load(self.image).convert_alpha()
        self.rect = self.surface.get_rect()
        self.current_planet = None
        self.touching_planet = True

    def set_start_time(self, time):
        self.start_time = time

    def set_current_planet(self, planet):
        self.current_planet = planet

    def get_inputs(self):
        return

    def calc_planet_movement(self, duration):
        dist_to_nearest_planet = extramath.dist(self.position.xy, self.current_planet.position.xy)
        angle_to_nearest_planet = math.degrees(math.atan2(self.position.y-self.current_planet.get_y(), self.position.x-self.current_planet.get_x()))
        if dist_to_nearest_planet < self.current_planet.gravity_radius:
            expected_accel = Vector((dist_to_nearest_planet, angle_to_nearest_planet), vectortype.RTHETA)
            expected_veloc_change = expected_accel * duration
            expected_pos_change = self.velocity * duration + (expected_accel * duration * duration) / 2
            expected_dist_to_planet = extramath.dist((self.position + expected_pos_change).xy(), self.current_planet.position.xy)
            if expected_dist_to_planet - self.current_planet.size < self.collision_threshold:
                expected_pos_change = 0
                expected_veloc_change = Vector() - self.velocity
        else:
            return Vector((0, 0), vectortype.XY)


    def move(self, duration):
        planet_change = self.calc_planet_movement(duration)
        return

    def update(self, current_time):
        duration = current_time - self.start_time
        self.get_inputs()
        self.move(duration)
