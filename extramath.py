import math

def dist(point1, point2):
    distance = (math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))
    return distance

def avg(*args):
    sum = 0
    for item in args:
        sum += item
    return sum / len(args)