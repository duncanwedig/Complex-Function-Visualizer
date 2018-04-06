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
        # self.current_planet = None
        self.touching_planet = True
        self.current_offset = Vector((0,0), vectortype.XY)

    def set_start_time(self, time):
        self.start_time = time

    # def set_current_planet(self, planet):
    #     self.current_planet = planet

    def get_inputs(self):
        return

    def calc_planet_movement(self, duration, current_planet):
        dist_to_nearest_planet = -extramath.dist(self.position.xy, current_planet.position.xy)
        print(dist_to_nearest_planet)
        print(current_planet.size)
        angle_to_nearest_planet = math.degrees(math.atan2(self.position.y-current_planet.get_y(), self.position.x-current_planet.get_x()))
        if dist_to_nearest_planet < current_planet.gravity_size:
            if abs(dist_to_nearest_planet - current_planet.size) < self.collision_threshold and not self.touching_planet:
                self.touching_planet = True
                self.current_offset = Vector((dist_to_nearest_planet, angle_to_nearest_planet), vectortype.RTHETA)
            if self.touching_planet:
                return current_planet.position + self.current_offset
            else:
                expected_accel = Vector((dist_to_nearest_planet, angle_to_nearest_planet), vectortype.RTHETA)
                expected_veloc_change = expected_accel * duration
                expected_pos_change = self.velocity * duration + (expected_accel * duration * duration) / 2
                expected_dist_to_planet = extramath.dist((self.position + expected_pos_change).xy, current_planet.position.xy)
                if expected_dist_to_planet - current_planet.size < self.collision_threshold:
                    expected_veloc_change = current_planet.velocity - self.velocity
                    expected_pos_change = expected_veloc_change * duration
                return expected_pos_change
        else:
            return Vector((0, 0), vectortype.XY)


    def move(self, duration, current_planet):
        planet_change = self.calc_planet_movement(duration, current_planet)
        self.position = planet_change

        print(self.position)
        print(self.touching_planet)
        self.rect.move_ip(self.position.x - self.rect.x, self.position.y - self.rect.y)

    def update(self, screen, current_time, current_planet):
        duration = current_time - self.start_time
        self.get_inputs()
        self.move(duration, current_planet)
        screen.blit(self.surface, self.rect)
