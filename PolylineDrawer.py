from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class PolylineDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Polyline Drawer")
        self.points = []

        # Создание графика
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

        # Интерфейс для matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Обработка кликов мыши
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Кнопка для сброса точек
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()

    def on_click(self, event):
        if len(self.points) < 6:
            # Добавляем точку по клику
            self.points.append((event.xdata, event.ydata))
            self.ax.plot(event.xdata, event.ydata, 'ro')  # Рисуем точку
            if len(self.points) > 1:
                # Если есть хотя бы две точки, рисуем ломаную
                x_vals, y_vals = zip(*self.points)
                self.ax.plot(x_vals, y_vals, 'b-')
            self.canvas.draw()
        else:
            print("All 6 points have been selected.")

    def reset(self):
        self.points = []
        self.ax.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.canvas.draw()