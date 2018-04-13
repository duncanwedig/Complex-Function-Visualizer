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
        self.scale = (x/window[0][1], y/window[0][1])
        self.lower = window[1][0]
        self.left = window[0][0]
        self.upper = window[1][1]
        self.right = window[0][1]
        self.x_axis = avg(self.lower, self.upper) * self.scale[1]
        self.y_axis = avg(self.left, self.right) * self.scale[0]

        self.interval = interval

        self.x_locations = np.array([x for x in np.arange(self.left, self.right + self.interval, self.interval)])
        self.y_locations = np.array([y for y in np.arange(self.lower, self.upper + self.interval, self.interval)])

        self.original_lattice = np.array([[[x, y] for x in np.arange(self.left, self.right + self.interval, self.interval)]
                                for y in np.arange(self.lower, self.upper + self.interval, self.interval)])
        # print(self.original_lattice)


    def connect_original_points(self, screen, line_width=2, color=(0, 0, 0)):
        # pygame.draw.line(screen, color, (self.left, self.lower), (self.left, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.right, self.lower), (self.right, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.left, self.upper), (self.right, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.left, self.lower), (self.right, self.lower), line_width)
        for x in self.x_locations:
            pygame.draw.line(screen, color, (x, self.lower), (x, self.upper), line_width)
        for y in self.y_locations:
            pygame.draw.line(screen, color, (y, self.lower), (y, self.upper), line_width)

        self.draw_axes(screen, color=color)

    def draw_axes(self, screen, line_width=4, color=(0, 0, 0)):
        pygame.draw.line(screen, (0, 0, 255), (self.y_axis, self.lower * self.scale[1]), (self.y_axis, self.upper * self.scale[1]), line_width)
        pygame.draw.line(screen, (0, 0, 255), (self.left * self.scale[0], self.x_axis), (self.right * self.scale[0], self.x_axis), line_width)


class ComplexGrid(Grid):

    def __init__(self, window=((0, 20), (0, 20)), interval=1, step=.01):
        self.step = step
        super().__init__(window, interval)
        # self.complex_points = np.array([[complex(item[0], item[1]) for item in self.original_lattice[column]]
        #                                   for column in np.arange(len(self.original_lattice))])
        self.complex_points = np.array([[complex(x - self.unscaled_y_ax, y - self.unscaled_x_ax) for x in np.arange(self.left, self.right + self.interval, self.interval)]
                                          for y in np.arange(self.lower, self.upper + self.interval, self.interval)])

        self.func = np.vectorize(self.specialfunc)
        self.complex_points = self.func(self.complex_points)

    def specialfunc(self, number=complex(1,0)):
        return number**2

    def complexdraw(self, screen, color=(0,0,0), line_width=4):
        for a, y in enumerate(self.complex_points):
            for b, x in enumerate(self.complex_points):
                x_point = self.complex_points[a][b].real * self.scale[0] + 500
                y_point = self.complex_points[a][b].imag * self.scale[1] + 500
                xy_point = (x_point, y_point)

                orig_x_point = self.original_lattice[a][b][0] - self.unscaled_x_ax
                orig_y_point = self.original_lattice[a][b][1] - self.unscaled_y_ax
                orig_xy_point = (orig_x_point, orig_y_point)

                if b < len(self.complex_points[a])-1:
                    x_right = self.complex_points[a][b+1].real * self.scale[0] + 500
                    y_right = self.complex_points[a][b+1].imag * self.scale[1] + 500
                    xy_right = (x_right, y_right)

                    orig_x_right = self.original_lattice[a][b + 1][0] - self.unscaled_x_ax
                    orig_y_right = self.original_lattice[a][b + 1][1] - self.unscaled_y_ax
                    orig_xy_right = (orig_x_right, orig_y_right)

                    for t in np.arange(1, int(1/self.step + 1)):
                        current_complex_point = self.func(
                            complex(*lerp(orig_xy_right, orig_xy_point, t * self.step)))
                        past_complex_point = self.func(
                            complex(*lerp(orig_xy_right, orig_xy_point, (t - 1) * self.step)))

                        pygame.draw.line(screen, color,
                                         (current_complex_point.real * self.scale[0] + 500,
                                          current_complex_point.imag * self.scale[1] + 500),
                                         (past_complex_point.real * self.scale[0] + 500,
                                          past_complex_point.imag * self.scale[1] + 500), line_width)
                    # pygame.draw.line(screen, color, xy_point, xy_right, line_width)
                if a < len(self.complex_points)-1:
                    x_lower = self.complex_points[a + 1][b].real * self.scale[0] + 500
                    y_lower = self.complex_points[a + 1][b].imag * self.scale[1] + 500
                    xy_lower = (x_lower, y_lower)

                    orig_x_lower = self.original_lattice[a + 1][b][0] - self.unscaled_x_ax
                    orig_y_lower = self.original_lattice[a + 1][b][1] - self.unscaled_y_ax
                    orig_xy_lower = (orig_x_lower, orig_y_lower)

                    for t in np.arange(1, int(1/self.step + 1)):
                        current_complex_point = self.func(
                            complex(*lerp(orig_xy_lower, orig_xy_point, t * self.step)))
                        past_complex_point = self.func(
                            complex(*lerp(orig_xy_lower, orig_xy_point, (t - 1) * self.step)))
                        pygame.draw.line(screen, color,
                                         (current_complex_point.real * self.scale[0] + 500,
                                          current_complex_point.imag * self.scale[1] + 500),
                                         (past_complex_point.real * self.scale[0] + 500,
                                          past_complex_point.imag * self.scale[1] + 500), line_width)


class PolynomialGrid(ComplexGrid):

    def __init__(self, window=((0, 20), (0, 20)), interval=1, step=.01, coefficients=(0,0,1)):
        self.coefficients = coefficients
        super().__init__(window, interval, step)

    def specialfunc(self, number=complex(1,0)):
        sum = 0
        for power, coefficient in enumerate(self.coefficients):
            sum += (number ** power) * coefficient * self.interval
        return sum


class ExponentialGrid(ComplexGrid):

        def __init__(self, window=((0, 20), (0, 20)), interval=1, step=.01, base=cmath.e):
            self.base = base
            super().__init__(window, interval, step)

        def specialfunc(self, number=complex(1, 0)):
            return (cmath.exp(number * cmath.log(self.base)))


size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)

vis = PolynomialGrid()

screen.fill([255, 255, 255])
vis.connect_original_points(screen)
# vis.complexdraw(screen, color=(255,0,0))

pygame.display.flip()


while 1:
    time.sleep(1)
    pass
