import numpy as np

from math import cos, sin, radians


class Cube:
    def __init__(self, points, color):
        self.color = color
        self.points = points
        self.max_point = self.found_max_point()
        self.rotate_matrix = None
    def found_max_point(self):
        max_point = self.points[0][0]
        for point in self.points:
            curr = max(point)
            if max_point < curr:
                max_point = curr
        return max_point

    def getFaces(self):
        vertices = np.array(self.points)
        return [[vertices[j] for j in [0, 1, 2, 3]],
                 [vertices[j] for j in [4, 5, 6, 7]],
                 [vertices[j] for j in [0, 3, 7, 4]],
                 [vertices[j] for j in [1, 2, 6, 5]],
                 [vertices[j] for j in [0, 1, 5, 4]],
                 [vertices[j] for j in [2, 3, 7, 6]]]


    def rotate(self, angel, axis):
        """angel указывается числом в градусах
           axis указывается строкой из одного символа \"x\",\"z\,\"y\"
           """

        angel = radians(angel)
        self.add1()
        if axis == "y":
            self.rotate_matrix = [[cos(angel), sin(angel), 0, 0],
                             [-1 * sin(angel), cos(angel), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]]
            color = "green"
        elif axis == "z":
            self.rotate_matrix = [[1, 0, 0, 0],
                             [0, cos(angel), sin(angel), 0],
                             [0, -1 * sin(angel), cos(angel), 0],
                             [0, 0, 0, 1]]
            color = "red"
        elif axis == "x":
            self.rotate_matrix = [[cos(angel), 0, -1 * sin(angel), 0],
                             [0, 1, 0, 0],
                             [sin(angel), 0, cos(angel), 0],
                             [0, 0, 0, 1]]
            color = "yellow"
        else:
            raise Exception("Такой оси не существует!")

        new_points = self.multiply()
        new_cube = Cube(new_points,color)
        new_cube.remove1()
        self.remove1()
        return new_cube
    def multiply(self):
        p_rows = len(self.points)
        p_columns = len(self.points[0])
        r_rows = len(self.rotate_matrix)
        r_columns = len(self.rotate_matrix[0])
        if(p_columns != r_rows):
            raise Exception("Чета матрицы сломались какта")
        new_points = [[0 for i in range(r_columns)] for j in range(p_rows)]
        for i in range(p_rows):
            for j in range(r_columns):
                for k in range(r_rows):
                    new_points[i][j] += self.points[i][k]*self.rotate_matrix[k][j]
        return new_points
    def add1(self):
        for point in self.points:
            point.append(1)
    def remove1(self):
        for point in self.points:
            point.pop(-1)
