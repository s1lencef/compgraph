"""Сформировать на плоскости параболический сплайн на основе зада-
ющей ломаной, определяемой 5 или большим количеством точек. Обеспе-
чить редактирование координат точек задающей ломаной кривой с перерисо-
вкой сплайна"""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PolylineDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Polyline Drawer")
        self.points = []

        # Создание графика
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 20)

        # Интерфейс для matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Обработка кликов мыши
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Кнопка для сброса точек
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()
        self.draw_button = tk.Button(root, text="Draw", command=self.reset)
        self.draw_button.pack()

    def on_click(self, event):
        # Добавляем точку по клику
        self.points.append((event.xdata, event.ydata))
        self.ax.plot(event.xdata, event.ydata, 'ro')
        print(self.points)# Рисуем точку
        if len(self.points) > 1:
            # Если есть хотя бы две точки, рисуем ломаную
            x_vals, y_vals = zip(*self.points)
            self.ax.plot(x_vals, y_vals, 'b-')
        self.canvas.draw()


    def reset(self):
        self.points = []
        self.ax.clear()
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 20)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PolylineDrawer(root)
    root.mainloop()
