import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import TextBox, Button


class CubeFactory:
    def __init__(self, cube):
        self.max_point = 0
        self.ax = None
        self.x_box = None
        self.y_box = None
        self.curr = cube
        self.first = True

    def draw(self, *cubes):

        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.35)
        self.ax = fig.add_subplot(111, projection='3d')
        i = 0
        for cube in cubes:
            if (i == 0):
                curr = cube
                i += 1
            self.ax.add_collection3d(
                Poly3DCollection(cube.getFaces(), facecolors=cube.color, linewidths=1, edgecolors=cube.color, alpha=.5))
            if cube.max_point > self.max_point:
                self.max_point = cube.max_point
        self.ax.set_xlim([-1 * (self.max_point + 3), self.max_point + 3])
        self.ax.set_ylim([-1 * (self.max_point + 3), self.max_point + 3])
        self.ax.set_zlim([-1 * (self.max_point + 3), self.max_point + 3])

        self.ax.set_xlabel('Z')
        self.ax.set_ylabel('X')
        self.ax.set_zlabel('Y')

        self.ax.quiver(0, 0, 0, self.max_point + 5, 0, 0, color='red', arrow_length_ratio=0.1)  # Ось X (красная)
        self.ax.quiver(0, 0, 0, 0, self.max_point + 5, 0, color='yellow', arrow_length_ratio=0.1)  # Ось Y (зелёная)
        self.ax.quiver(0, 0, 0, 0, 0, self.max_point + 5, color='green', arrow_length_ratio=0.1)  # Ось Z (синяя)

        # Поле ввода для оси X
        axbox_x = plt.axes([0.2, 0.2, 0.1, 0.05])
        self.x_box = TextBox(axbox_x, "Угол поворота:")

        # Поле ввода для оси Y
        axbox_y = plt.axes([0.2, 0.1, 0.1, 0.05])
        self.y_box = TextBox(axbox_y, "Ось:")

        # Кнопка для обновления графика
        axbutton = plt.axes([0.45, 0.01, 0.15, 0.05])
        button = Button(axbutton, 'отрисовать')

        button.on_clicked(self.update_graph)

        plt.show()


    def update_graph(self, event):
        plt.close()
        self.first = False
        print(self.x_box.text + "  " + self.y_box.text)
        angel = int(self.x_box.text)
        axis = self.y_box.text

        rotated_cube = self.curr.rotate(angel, axis)
        # Очищаем старый график
        self.ax.clear()

        self.draw(self.curr, rotated_cube)
