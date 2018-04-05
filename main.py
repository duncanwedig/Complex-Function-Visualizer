import planet, player, pygame, random

class Main(object):
    
    def __init__(self, time):
        self.start_time = time
    
    def update(self, time):
        planet_size = random.randint(100, 150)
        pass