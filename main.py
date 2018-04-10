import pygame, random, sys, time, visualize
from vector import Vector, vectortype
import numpy as np


size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)

x = 20
y = 20
h = 80

# while 1:
#    time.sleep(0.05)
#    screen.fill([0, 255, 0])
#    pygame.draw.line(screen, (0, 0, 255), (x, y), (x + h, y + h), 2)
#    pygame.display.flip()
#    h += -1

vis = visualize.PolynomialGrid()
screen.fill([255, 255, 255])
vis.connect_original_points(screen)
pygame.display.flip()

for n in range(2):
    screen.fill([255, 255, 255])
    vis.connect_original_points(screen)
    vis.polydraw(screen, color=(255,0,0))

    pygame.display.flip()

print(np.array([[complex(x-500, y-500) for x in range(0, 1000 + 10, 10)] for y in range(0, 1000 + 10, 10)]))

while 1:
    pass


# screen = pygame.display.set_mode([960, 720])