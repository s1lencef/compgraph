"""Сформировать на плоскости параболический сплайн на основе зада-
ющей ломаной, определяемой 5 или большим количеством точек. Обеспе-
чить редактирование координат точек задающей ломаной кривой с перерисо-
вкой сплайна"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

# Изначальные точки
points = np.array([[0, 0], [1, 2], [2, 0], [3, 3], [4, 1]])


def parabolic_spline(points):
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


class SplineEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Параболический сплайн")

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.points_plot, = self.ax.plot([], [], 'ro-')
        self.spline_plot, = self.ax.plot([], [], 'b-')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

        self.text_boxes = []
        for i in range(5):
            entry = tk.Entry(self)
            entry.insert(0, f'{points[i][0]},{points[i][1]}')
            entry.pack(pady=5)
            self.text_boxes.append(entry)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        update_button = tk.Button(button_frame, text="Update Points", command=self.update_points)
        update_button.grid(row=0, column=0, padx=5)

        line_button = tk.Button(button_frame, text="Draw Line", command=self.draw_line)
        line_button.grid(row=0, column=1, padx=5)

        spline_button = tk.Button(button_frame, text="Draw Spline", command=self.draw_spline)
        spline_button.grid(row=0, column=2, padx=5)

        self.update_plots()

    def update_plots(self):
        self.points_plot.set_data(points[:, 0], points[:, 1])
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def update_points(self):
        global points
        try:
            new_points = []
            for entry in self.text_boxes:
                x, y = map(float, entry.get().split(','))
                new_points.append((x, y))
            points = np.array(new_points)
            self.update_plots()
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, используйте формат (x,y).")

    def draw_line(self):
        self.points_plot.set_data(points[:, 0], points[:, 1])
        self.update_plots()

    def draw_spline(self):
        spline_points = parabolic_spline(points)
        self.spline_plot.set_data(spline_points[:, 0], spline_points[:, 1])
        self.update_plots()


if __name__ == '__main__':
    app = SplineEditor()
    app.mainloop()


