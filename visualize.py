import math, extramath, pygame, cmath
import numpy as np
from vector import Vector, vectortype


class Grid(object):

    def __init__(self, window=((0, 20), (0, 20)), interval=1):
        x,y = pygame.display.get_surface().get_size()
        self.scale = (x/window[0][1], y/window[0][1])
        self.lower = window[1][0]
        self.left = window[0][0]
        self.upper = window[1][1]
        self.right = window[0][1]
        self.x_axis = extramath.avg(self.lower, self.upper) * self.scale[1]
        self.y_axis = extramath.avg(self.left, self.right) * self.scale[0]
        self.unscaled_y_ax = self.y_axis / self.scale[0]
        self.unscaled_x_ax = self.x_axis / self.scale[1]

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
                x_point = self.original_lattice[a][b][0] * self.scale[0]
                y_point = self.original_lattice[a][b][1] * self.scale[1]
                if b < len(self.original_lattice[a])-1:
                    x_right = self.original_lattice[a][b+1][0] * self.scale[0]
                    y_right = self.original_lattice[a][b+1][1] * self.scale[1]
                    pygame.draw.line(screen, color, (x_point, y_point), (x_right, y_right), line_width)
                if a < len(self.original_lattice)-1:
                    x_lower = self.original_lattice[a+1][b][0] * self.scale[0]
                    y_lower = self.original_lattice[a+1][b][1] * self.scale[1]
                    pygame.draw.line(screen, color, (x_point, y_point), (x_lower, y_lower), line_width)

        self.draw_axes(screen, color=color)

    def draw_axes(self, screen, line_width=4, color=(0, 0, 0)):
        pygame.draw.line(screen, (0, 0, 255), (self.y_axis, self.lower * self.scale[1]), (self.y_axis, self.upper * self.scale[1]), line_width)
        pygame.draw.line(screen, (0, 0, 255), (self.left * self.scale[0], self.x_axis), (self.right * self.scale[0], self.x_axis), line_width)

class ComplexGrid(Grid):

    def __init__(self, window=((0, 20), (0, 20)), interval=1, step=.01):
        super().__init__(window, interval)

class PolynomialGrid(Grid):

    def __init__(self, window=((0, 20), (0, 20)), interval=1, step=.01, coefficients=(0,0,1)):
        self.coefficients = coefficients
        self.step = step
        super().__init__(window, interval)
        # self.complex_points = np.array([[complex(item[0], item[1]) for item in self.original_lattice[column]]
        #                                   for column in range(len(self.original_lattice))])
        self.complex_points = np.array([[complex(x - self.unscaled_y_ax, y - self.unscaled_x_ax) for x in range(self.left, self.right + self.interval, self.interval)]
                                          for y in range(self.lower, self.upper + self.interval, self.interval)])

        self.func = np.vectorize(self.specialfunc)
        self.complex_points = self.func(self.complex_points)

    def specialfunc(self, number=complex(1,0)):
        sum = 0
        for power, coefficient in enumerate(self.coefficients):
            sum += (number ** power) * coefficient * self.interval
        return sum

    def polydraw(self, screen, color=(0,0,0), line_width=4):
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

                    for t in range(1, 100):
                        current_complex_point = self.func(
                            complex(*extramath.lerp(orig_xy_right, orig_xy_point, t * self.step)))
                        past_complex_point = self.func(
                            complex(*extramath.lerp(orig_xy_right, orig_xy_point, (t - 1) * self.step)))

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

                    for t in range(1, 100):
                        current_complex_point = self.func(
                            complex(*extramath.lerp(orig_xy_lower, orig_xy_point, t * self.step)))
                        past_complex_point = self.func(
                            complex(*extramath.lerp(orig_xy_lower, orig_xy_point, (t - 1) * self.step)))
                        pygame.draw.line(screen, color,
                                         (current_complex_point.real * self.scale[0] + 500,
                                          current_complex_point.imag * self.scale[1] + 500),
                                         (past_complex_point.real * self.scale[0] + 500,
                                          past_complex_point.imag * self.scale[1] + 500), line_width)

                    # pygame.draw.line(screen, color, xy_point, xy_lower, line_width)
        print('yayayyayayayayay')

class ExponentialGrid(Grid):

        def __init__(self, window=((0, 20), (0, 20)), interval=1, step=.01, base=cmath.e):
            self.base = base
            self.step = step
            super().__init__(window, interval)
            # self.complex_points = np.array([[complex(item[0], item[1]) for item in self.original_lattice[column]]
            #                                   for column in range(len(self.original_lattice))])
            self.complex_points = np.array([[complex(x - self.unscaled_y_ax, y - self.unscaled_x_ax) for x in
                                             range(self.left, self.right + self.interval, self.interval)]
                                            for y in range(self.lower, self.upper + self.interval, self.interval)])

            self.expfunc = np.vectorize(self.exponentiate)
            self.complex_points = self.expfunc(self.complex_points)

        def exponentiate(self, number=complex(1, 0)):
            return (cmath.exp(number * cmath.log(self.base)))

        def expdraw(self, screen, color=(0, 0, 0), line_width=4):
            for a, y in enumerate(self.complex_points):
                for b, x in enumerate(self.complex_points):
                    x_point = self.complex_points[a][b].real * self.scale[0] + 500
                    y_point = self.complex_points[a][b].imag * self.scale[1] + 500
                    xy_point = (x_point, y_point)

                    orig_x_point = self.original_lattice[a][b][0] - self.unscaled_x_ax
                    orig_y_point = self.original_lattice[a][b][1] - self.unscaled_y_ax
                    orig_xy_point = (orig_x_point, orig_y_point)

                    if b < len(self.complex_points[a]) - 1:
                        x_right = self.complex_points[a][b + 1].real * self.scale[0] + 500
                        y_right = self.complex_points[a][b + 1].imag * self.scale[1] + 500
                        xy_right = (x_right, y_right)

                        orig_x_right = self.original_lattice[a][b + 1][0] - self.unscaled_x_ax
                        orig_y_right = self.original_lattice[a][b + 1][1] - self.unscaled_y_ax
                        orig_xy_right = (orig_x_right, orig_y_right)

                        for t in range(1, 100):
                            current_complex_point = self.expfunc(
                                complex(*extramath.lerp(orig_xy_right, orig_xy_point, t * self.step)))
                            past_complex_point = self.expfunc(
                                complex(*extramath.lerp(orig_xy_right, orig_xy_point, (t - 1) * self.step)))

                            pygame.draw.line(screen, color,
                                             (current_complex_point.real * self.scale[0] + 500,
                                              current_complex_point.imag * self.scale[1] + 500),
                                             (past_complex_point.real * self.scale[0] + 500,
                                              past_complex_point.imag * self.scale[1] + 500), line_width)
                        # pygame.draw.line(screen, color, xy_point, xy_right, line_width)
                    if a < len(self.complex_points) - 1:
                        x_lower = self.complex_points[a + 1][b].real * self.scale[0] + 500
                        y_lower = self.complex_points[a + 1][b].imag * self.scale[1] + 500
                        xy_lower = (x_lower, y_lower)

                        orig_x_lower = self.original_lattice[a + 1][b][0] - self.unscaled_x_ax
                        orig_y_lower = self.original_lattice[a + 1][b][1] - self.unscaled_y_ax
                        orig_xy_lower = (orig_x_lower, orig_y_lower)

                        for t in range(1, 100):
                            current_complex_point = self.expfunc(
                                complex(*extramath.lerp(orig_xy_lower, orig_xy_point, t * self.step)))
                            past_complex_point = self.expfunc(
                                complex(*extramath.lerp(orig_xy_lower, orig_xy_point, (t - 1) * self.step)))
                            pygame.draw.line(screen, color,
                                             (current_complex_point.real * self.scale[0] + 500,
                                              current_complex_point.imag * self.scale[1] + 500),
                                             (past_complex_point.real * self.scale[0] + 500,
                                              past_complex_point.imag * self.scale[1] + 500), line_width)
