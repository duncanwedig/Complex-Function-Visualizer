import math

def dist(point1, point2):
    distance = (math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))
    return distance

def avg(*args):
    sum = 0
    for item in args:
        sum += item
    return sum / len(args)

def lerp(p1, p2, t):
    x = ((p2[0] - p1[0]) * t) + p1[0]
    y = ((p2[1] - p1[1]) * t) + p1[1]
    return (x, y)