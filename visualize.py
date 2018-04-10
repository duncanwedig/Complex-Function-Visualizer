import math, extramath, pygame, cmath
import numpy as np
from vector import Vector, vectortype


class Grid(object):

    def __init__(self, window=((0, 1000), (0, 1000)), interval=100):
        self.lower = window[1][0]
        self.left = window[0][0]
        self.upper = window[1][1]
        self.right = window[0][1]
        self.x_axis = extramath.avg(self.lower, self.upper)
        self.y_axis = extramath.avg(self.left, self.right)

        self.interval = interval

        self.original_lattice = np.array([[[x, y] for x in range(self.left, self.right + self.interval, self.interval)]
                                for y in range(self.lower, self.upper + self.interval, self.interval)])
        # print(self.original_lattice)


    def connect_original_points(self, screen, line_width=2, color=(0, 0, 0)):
        # pygame.draw.line(screen, color, (self.left, self.lower), (self.left, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.right, self.lower), (self.right, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.left, self.upper), (self.right, self.upper), line_width)
        # pygame.draw.line(screen, color, (self.left, self.lower), (self.right, self.lower), line_width)
        for a, y in enumerate(self.original_lattice):
            for b, x in enumerate(self.original_lattice):
                x_point = self.original_lattice[a][b][0]
                y_point = self.original_lattice[a][b][1]
                if b < len(self.original_lattice[a])-1:
                    x_right = self.original_lattice[a][b+1][0]
                    y_right = self.original_lattice[a][b+1][1]
                    pygame.draw.line(screen, color, (x_point, y_point), (x_right, y_right), line_width)
                if a < len(self.original_lattice)-1:
                    x_lower = self.original_lattice[a+1][b][0]
                    y_lower = self.original_lattice[a+1][b][1]
                    pygame.draw.line(screen, color, (x_point, y_point), (x_lower, y_lower), line_width)

        self.draw_axes(screen, color=color)

    def draw_axes(self, screen, line_width=4, color=(0, 0, 0)):
        pygame.draw.line(screen, (0, 0, 255), (self.y_axis, self.lower), (self.y_axis, self.upper), line_width)
        pygame.draw.line(screen, (0, 0, 255), (self.left, self.x_axis), (self.right, self.x_axis), line_width)



class PolynomialGrid(Grid):

    def __init__(self, window=((0, 1000), (0, 1000)), interval=100, step=10, coefficients=(0,0,1)):
        self.coefficients = coefficients
        self.step = step
        super().__init__(window, interval)
        # self.complex_points = np.array([[complex(item[0], item[1]) for item in self.original_lattice[column]]
        #                                   for column in range(len(self.original_lattice))])
        self.complex_points = np.array([[complex(x - self.y_axis, y - self.x_axis) for x in range(self.left, self.right + self.step, self.step)]
                                          for y in range(self.lower, self.upper + self.step, self.step)])
        self.complex_points = np.array([[complex(x-500, y-500) for x in range(0, 1000 + 10, 10)] for y in range(0, 1000 + 10, 10)])
        print(self.y_axis)
        print(self.x_axis)
        print(self.left)
        print(self.right)
        print(self.lower)
        print(self.upper)
        print(self.step)

        polyfunc = np.vectorize(self.polynomialify)
        print(polyfunc(self.complex_points))
        self.complex_points = polyfunc(self.complex_points)

        print(self.complex_points)

    def polynomialify(self, number=complex(1,0)):
        sum = 0
        for power, coefficient in enumerate(self.coefficients):
            sum += (number ** power) * coefficient * self.interval
        return sum

    def polydraw(self, screen, color=(0,0,0), line_width=4):
        for a, y in enumerate(self.complex_points):
            for b, x in enumerate(self.complex_points):
                x_point = self.complex_points[a][b].real + 500
                y_point = self.complex_points[a][b].imag + 500
                print(x_point)
                print(y_point)
                if b < len(self.complex_points[a])-1:
                    x_right = self.complex_points[a][b+1].real + 500
                    y_right = self.complex_points[a][b+1].imag + 500
                    pygame.draw.line(screen, color, (x_point, y_point), (x_right, y_right), line_width)
                if a < len(self.complex_points)-1:
                    x_lower = self.complex_points[a+1][b].real + 500
                    y_lower = self.complex_points[a+1][b].imag + 500
                    pygame.draw.line(screen, color, (x_point, y_point), (x_lower, y_lower), line_width)
