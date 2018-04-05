import planet, player, pygame, random, sys, time
from vector import Vector, vectortype

class Main(object):
    
    def __init__(self, time):
        self.start_time = time
    
    def update(self, time):
        planet_size = random.randint(100, 150)
        pass


screen = pygame.display.set_mode([960, 720])
ball = pygame.image.load("ball.png")
location = Vector((300.0, 300.0), vectortype.XY)
planet = planet.Planet(location, 128, 256)
velocity = [-1, -1]
switch = False

current_time = time.clock()
planet.set_start_time(current_time)
while 1:
    prev_time = current_time
    current_time = time.clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill([0, 255, 0])
    planet.update(screen, time.clock())
    if time.clock() > 5:
        if not switch:
            planet2 = planet.Planet(location, 128, 256)
            switch = True
        else:
            planet2.update(screen, time.clock())
    pygame.display.flip()
    print(planet.velocity)
    print(planet.position)
    print(planet.rect)