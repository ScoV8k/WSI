import numpy as np
import random
from matplotlib import pyplot as plt


class Solver():
    def __init__(self, func, gradient):
        self.func = func
        self.gradient = gradient
        self.points = 0
        self.b = 0
        self.x0 = 0

    def set_points(self, new_points):
        self.points = new_points

    def set_b(self, new_b):
        self.b = new_b

    def set_x0(self, new_x0):
        self.x0 = new_x0

    def get_parameters(self):
        return {'function': self.func, 'gradient': self.gradient, 'b': self.b, 'x0': self.x0}

    def gradient_descent(self, x0, b, t=0.0001):
        vector = x0
        points = [x0]
        while True:
            d = -b * self.gradient(vector)
            vector = vector + d
            points.append(vector)
            if isinstance(vector, (int, float)):
                if np.abs(d) <= t:
                    break
            else:
                if np.abs(d[0]) <= t and np.abs(d[1]) <= t:
                    break
        self.set_points(points)
        self.set_b(b)
        self.set_x0(x0)

    def make_plot(self, range):
        points = np.array(self.points)
        xpts = np.linspace(-range, range, 1000)
        plt.plot(xpts, self.func(xpts))
        plt.plot(points, self.func(points), marker='o')
        plt.title(f'learn rate={self.b}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.show()


    def make_contour(self, range, dim=2):
        x, y = np.meshgrid(np.linspace(-range, range, 100), np.linspace(-range, range, 100))
        xy = x, y
        pointsx = []
        pointsy = []
        pointsz = []
        for element in self.points:
            pointsx.append(element[0])
            pointsy.append(element[1])
            pointsz.append(self.func(element))
        if dim == 3:
            fig = plt.figure()
            ax = plt.axes(projection='3d')
            ax.contour(x, y, self.func(xy), levels=30)
            ax.plot(pointsx, pointsy, pointsz, c='red', marker='o',  linewidth=3)
        else:
            plt.contour(x, y, self.func(xy))
            plt.plot(pointsx, pointsy, marker='o')
            plt.scatter(self.x0[0], self.x0[1], c='red')
        plt.title(f'learn rate={self.b}, x0=({self.x0[0]:.2f},{self.x0[1]:.2f})')
        plt.show()

def func1(v):
    return 0.25 * v ** 4

def grad1(v):
    return v**3

def func2(v):
    x = v[0]
    y = v[1]
    return 2 - np.exp(-x**2-y**2) - 0.5 * np.exp(-(x + 1.5)**2 - (y - 2)**2)

def grad2(v):
    x = v[0]
    y = v[1]
    x1=2*x*np.exp(-x**2-y**2) + (x + 1.5) * np.exp(-(x+1.5)**2 - (y - 2)**2)
    x2=2*y*np.exp(-x**2-y**2) + (y + 1.5) * np.exp(-(x+1.5)**2 - (y - 2)**2)
    result = np.array([x1, x2])
    return result

# solver = Solver(func1, grad1)
# solver.gradient_descent(4, 4)
# solver.make_plot(4)
solver2 = Solver(func2, grad2)
solver2.gradient_descent(np.array([random.uniform(-2, 2), random.uniform(-2, 2)]), random.choice([0.05, 0.5, 0.9]))
solver2.make_contour(4)
# print(solver2.get_parameters())