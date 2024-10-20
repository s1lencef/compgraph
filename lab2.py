"""Сформировать на плоскости параболический сплайн на основе зада-
ющей ломаной, определяемой 5 или большим количеством точек. Обеспе-
чить редактирование координат точек задающей ломаной кривой с перерисо-
вкой сплайна"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox

# Изначальные точки
points = np.array([[0, 0], [1, 2], [2, 0], [3, 3], [4, 1]])


def parabolic_spline(points):
    """Генерация параболического сплайна на основе заданных точек."""
    n = len(points)
    spline_points = []

    for i in range(n - 1):
        p0, p1 = points[i], points[i + 1]
        if i < n - 2:
            p2 = points[i + 2]
            coeffs = np.polyfit([p0[0], p1[0], p2[0]], [p0[1], p1[1], p2[1]], 2)
        else:
            coeffs = np.polyfit([p0[0], p1[0]], [p0[1], p1[1]], 1)

        x_vals = np.linspace(p0[0], p1[0], 100)
        y_vals = np.polyval(coeffs, x_vals)
        spline_points.append(np.column_stack((x_vals, y_vals)))

    return np.vstack(spline_points)


class SplineEditor:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Параболический сплайн')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.points_plot, = self.ax.plot([], [], 'ro-')  # Точки ломаной
        self.spline_plot, = self.ax.plot([], [], 'b-')  # Сплайн

        self.text_boxes = []
        for i in range(5):
            ax_text = plt.axes([0.1, 1 - i * 0.1, 0.03, 0.03])
            text_box = TextBox(ax_text, f'Point {i + 1} (x,y)', initial=f'{points[i][0]},{points[i][1]}')
            self.text_boxes.append(text_box)

        # Кнопка для обновления
        self.update_button_ax = plt.axes([0.81, 0.9, 0.15, 0.05])
        self.update_button = Button(self.update_button_ax, 'Update Points')
        self.update_button.on_clicked(self.update_points)

        # Кнопка для отрисовки ломанной
        self.line_button_ax = plt.axes([0.81, 0.75, 0.15, 0.05])
        self.line_button = Button(self.line_button_ax, 'Draw Line')
        self.line_button.on_clicked(self.draw_line)

        # Кнопка для отрисовки сплайна
        self.spline_button_ax = plt.axes([0.81, 0.6, 0.15, 0.05])
        self.spline_button = Button(self.spline_button_ax, 'Draw Spline')
        self.spline_button.on_clicked(self.draw_spline)

        self.update_plots()

    def update_plots(self):
        """Обновление отображаемых графиков."""
        self.points_plot.set_data(points[:, 0], points[:, 1])
        self.ax.relim()
        self.ax.autoscale_view()
        plt.draw()

    def update_points(self, event):
        """Обновление точек ломаной из текстовых полей."""
        global points
        try:
            new_points = []
            for text_box in self.text_boxes:
                x, y = map(float, text_box.text.split(','))
                new_points.append((x, y))
            points = np.array(new_points)
            self.update_plots()
        except ValueError:
            print("Ошибка ввода. Пожалуйста, используйте формат (x,y).")

    def draw_line(self, event):
        """Отрисовка ломаной."""
        self.points_plot.set_data(points[:, 0], points[:, 1])
        self.update_plots()

    def draw_spline(self, event):
        """Отрисовка сплайна."""
        spline_points = parabolic_spline(points)
        self.spline_plot.set_data(spline_points[:, 0], spline_points[:, 1])
        self.update_plots()


if __name__ == '__main__':
    editor = SplineEditor()
    plt.show()

