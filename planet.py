import sys, pygame, time
import vector
pygame.init()


class Planet(object):
    
    #self.velocity = vector.Vector([-1,0], vector.vectortype.XY)
    #self.start_time = 0
    
    def __init__(self, location, radius, gravity_radius):
        super().__init__()
        self.rect = pygame.Rect(location, (radius*2, radius*2))
        self.size = radius
        self.gravity_size = gravity_radius
        self.surface = pygame.Surface()
        self.gravity_image = pygame
        pass
    
    def set_start_time(self, time):
        self.start_time = time
    
    def move(self, duration):
        self.rect.move_ip(*((self.velocity * duration).xy()))
    
    def get_blit_data(self):
        return ((self.surface, self.rect), ())
    
    def update(self, screen, current_time):
        self.move(current_time-self.start_time)
        screen.blit(*self.get_blit_data[0])
    
    

screen = pygame.display.set_mode([480, 360])
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()

velocity = [-1, -1]

while 1:
    time.sleep(0.05)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
    
    ballrect.move_ip(*velocity)
    
    screen.fill([0, 255, 0])
    screen.blit(ball, ballrect)
    pygame.display.flip()