import pygame, time, math, cmath
import numpy as np


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


class Grid(object):

    def __init__(self, window=((-10, 10), (-10, 10)), interval=1):
        x,y = pygame.display.get_surface().get_size()
        self.screen_center = [x/2, y/2]
        self.scale = (x/(window[0][1]-window[0][0]), y/(window[0][1]-window[0][0]))
        self.lower = window[1][0]
        self.left = window[0][0]
        self.upper = window[1][1]
        self.right = window[0][1]
        self.scaled_lower = 0
        self.scaled_left = 0
        self.scaled_upper = y
        self.scaled_right = x
        self.x_axis = avg(self.lower, self.upper)
        self.y_axis = avg(self.left, self.right)
        self.scaled_xax = self.x_axis * self.scale[1] + self.screen_center[1]
        self.scaled_yax = self.y_axis * self.scale[0] + self.screen_center[0]
        print(self.scaled_right)
        print(self.scaled_left)

        self.interval = interval

        self.x_locations = np.array([x for x in np.arange(self.y_axis, self.right + self.interval, self.interval)])
        self.y_locations = np.array([y for y in np.arange(self.x_axis, self.upper + self.interval, self.interval)])

        self.original_lattice = np.array([[[x, y] for x in np.arange(self.left, self.right + self.interval, self.interval)]
                                for y in np.arange(self.lower, self.upper + self.interval, self.interval)])
        # print(self.original_lattice)


    def connect_original_points(self, screen, line_width=2, color=(0, 0, 0)):
        # pygame.draw.line(screen, color, (self.left, self.lower), (self.left, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.right, self.lower), (self.right, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.left, self.upper), (self.right, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.left, self.lower), (self.right, self.lower), line_width)
        for x in self.scale_points(self.x_locations, False):
            pygame.draw.line(screen, color, (x, self.scaled_lower), (x, self.scaled_upper), line_width)
        for x in self.scale_points(self.x_locations, True):
            pygame.draw.line(screen, color, (x, self.scaled_lower), (x, self.scaled_upper), line_width)
        for y in self.scale_points(self.y_locations, False):
            pygame.draw.line(screen, color, (self.scaled_left, y), (self.scaled_right, y), line_width)
        for y in self.scale_points(self.y_locations, True):
            pygame.draw.line(screen, color, (self.scaled_left, y), (self.scaled_right, y), line_width)

        self.draw_axes(screen, color=color)

    def scale_point(self, number, isNegative=False):
        if isNegative:
            return -number * self.scale[0] + self.screen_center[0]
        else:
            return number * self.scale[0] + self.screen_center[0]

    def scale_points(self, numbers, isnegative=False):
        if isnegative:
            return np.array([-x * self.scale[0] + self.screen_center[0] for x in numbers])
        else:
            return np.array([x * self.scale[0] + self.screen_center[0] for x in numbers])

    def draw_axes(self, screen, line_width=4, color=(0, 0, 0)):
        pygame.draw.line(screen, (0, 0, 255), (self.scaled_yax, self.scaled_lower), (self.scaled_yax, self.scaled_upper), line_width)
        pygame.draw.line(screen, (0, 0, 255), (self.scaled_left * self.scale[0], self.scaled_xax), (self.scaled_right, self.scaled_xax), line_width)


class ComplexGrid(Grid):

    def __init__(self, window=((-10, 10), (-10, 10)), interval=1, step=.01):
        self.step = step
        super().__init__(window, interval)
        # self.complex_points = np.array([[complex(item[0], item[1]) for item in self.original_lattice[column]]
        #                                   for column in np.arange(len(self.original_lattice))])

        self.complex_xpoints = self.x_locations
        self.complex_ypoints = self.y_locations
        print(self.complex_ypoints)

        self.func = np.vectorize(self.specialfunc)
        self.make_real = np.vectorize(self.decomplexify)

    def complexify(self, points):
        complex_points = []
        for point in points:
            complex_points.append(complex(point[0], point[1]))
        return np.array(complex_points)

    def decomplexify(self, number):
        return (number.real, number.imag)

    def specialfunc(self, number):
        return number**2

    def complexdraw(self, screen, color=(0,0,0), line_width=4):
        for y in self.complex_ypoints:
            x_of_line = np.arange(self.left, self.right + self.step, self.step)
            yline = np.array([(x,y) for x in x_of_line])
            yline = self.complexify(yline)
            print(yline)
            yline = self.func(yline)

            for number, point in enumerate(yline):
                if 500.0 not in self.scale_points((point.real, point.imag), False):
                    pygame.draw.line(screen, color, self.scale_points((point.real, point.imag), False),
                                 self.scale_points((yline[number-1].real, yline[number-1].imag), False), line_width)

            for number, point in enumerate(yline):
                if 500.0 not in self.scale_points((point.real, point.imag), True):
                    pygame.draw.line(screen, color, self.scale_points((point.real, point.imag), True),
                                 self.scale_points((yline[number-1].real, yline[number-1].imag), True), line_width)

        for x in self.complex_xpoints:
            y_of_line = np.arange(self.lower, self.upper + self.step, self.step)
            xline = np.array([(x,y) for y in y_of_line])
            xline = self.complexify(xline)
            xline = self.func(xline)

            for number, point in enumerate(xline):
                if 500.0 not in self.scale_points((point.real, point.imag), False):
                    pygame.draw.line(screen, color, self.scale_points((point.real, point.imag), False),
                                 self.scale_points((xline[number-1].real, xline[number-1].imag), False), line_width)

            for number, point in enumerate(xline):
                if 500.0 not in self.scale_points((point.real, point.imag), True):
                    pygame.draw.line(screen, color, self.scale_points((point.real, point.imag), True),
                                 self.scale_points((xline[number-1].real, xline[number-1].imag), True), line_width)


        yline = np.arange(self.left, self.right + self.step, self.step)



        # for x in self.complex_xpoints:
        #     for t in np.arange(1/self.step + self.step):
        #         current_point = complex(*lerp((x, self.scaled_lower), (x, self.scaled_upper), self.step * t))
        #         pygame.draw.line(screen, color, lerp((x, self.scaled_lower), (x, self.scaled_upper), self.step * t),
        #                          lerp((x, self.scaled_lower), (x, self.scaled_upper), self.step * t - self.step),
        #                          line_width)
        #
        # for y in self.complex_ypoints:
        #     for t in np.arange(1/self.step + self.step):
        #         pygame.draw.line(screen, color, lerp((self.scaled_left, y), (self.scaled_right, y), self.step * t),
        #                          lerp((self.scaled_left, y), (self.scaled_right, y), self.step * t - self.step),
        #                          line_width)



class PolynomialGrid(ComplexGrid):

    def __init__(self, window=((-10, 10), (-10, 10)), interval=1, step=.01, coefficients=(0,0,1)):
        self.coefficients = coefficients
        super().__init__(window, interval, step)

    def specialfunc(self, number=complex(1,0)):
        sum = 0
        for power, coefficient in enumerate(self.coefficients):
            sum += (number ** power) * coefficient * self.interval
        return sum


class ExponentialGrid(ComplexGrid):

        def __init__(self, window=((-10, 10), (-10, 10)), interval=1, step=.01, base=cmath.e):
            self.base = base
            super().__init__(window, interval, step)

        def specialfunc(self, number=complex(1, 0)):
            return (cmath.exp(number * cmath.log(self.base)))


size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)

vis = ComplexGrid()

screen.fill([255, 255, 255])
vis.connect_original_points(screen)
vis.complexdraw(screen, color=(255,0,0))

# pygame.draw.line(screen, )

pygame.display.flip()


while 1:
    time.sleep(1)
    pass
