"""Сформировать билинейную поверхность на основе произвольного за-
дания ее четерех угловых точек. Обеспечить ее поворот относительно осей X
и Y"""


import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def rotate_surface(X, Y, Z, axis, angle):
    rad = np.radians(angle)

    if axis == 'X':
        rotation_matrix = np.array([[np.cos(rad), 0, np.sin(rad)],
                                    [0, 1, 0],
                                    [-np.sin(rad), 0, np.cos(rad)]])
    elif axis == 'Y':
        rotation_matrix = np.array([[np.cos(rad), -np.sin(rad), 0],
                                    [np.sin(rad), np.cos(rad), 0],
                                    [0, 0, 1]])
    else:
        return X, Y, Z

    points = np.array([X.flatten(), Y.flatten(), Z.flatten()])
    rotated_points = rotation_matrix @ points
    X_rotated = rotated_points[0].reshape(X.shape)
    Y_rotated = rotated_points[1].reshape(Y.shape)
    Z_rotated = rotated_points[2].reshape(Z.shape)

    return X_rotated, Y_rotated, Z_rotated


def parse_coordinates(entry):
    return list(map(float, entry.split(',')))


def draw_surface():
    coords1 = parse_coordinates(entry_point1.get())
    coords2 = parse_coordinates(entry_point2.get())
    coords3 = parse_coordinates(entry_point3.get())
    coords4 = parse_coordinates(entry_point4.get())

    x1, y1, z1 = coords1
    x2, y2, z2 = coords2
    x3, y3, z3 = coords3
    x4, y4, z4 = coords4

    x = np.linspace(min(x1, x2, x3, x4), max(x1, x2, x3, x4), 100)
    y = np.linspace(min(y1, y2, y3, y4), max(y1, y2, y3, y4), 100)
    X, Y = np.meshgrid(x, y)

    Z = (1 - (X - x1) / (x2 - x1)) * (1 - (Y - y1) / (y3 - y1)) * z1 + \
        ((X - x1) / (x2 - x1)) * (1 - (Y - y1) / (y3 - y1)) * z2 + \
        (1 - (X - x3) / (x4 - x3)) * ((Y - y1) / (y3 - y1)) * z3 + \
        ((X - x3) / (x4 - x3)) * ((Y - y1) / (y3 - y1)) * z4

    return X, Y, Z


def update_plot(X_list, Y_list, Z_list):
    for widget in window.pack_slaves():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']

    for i in range(len(X_list)):
        ax.plot_surface(X_list[i], Y_list[i], Z_list[i], cmap=colors[i % len(colors)], alpha=0.5)

    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_zlabel('Y')

    ax.quiver(0, 0, 0, 5, 0, 0, color='r', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 5, 0, color='g', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 5, color='b', arrow_length_ratio=0.1)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def on_draw():
    X, Y, Z = draw_surface()
    X_list.append(X)
    Y_list.append(Y)
    Z_list.append(Z)
    update_plot(X_list, Y_list, Z_list)


def on_rotate():
    axis = entry_axis.get().strip().upper()
    angle = float(entry_angle.get())

    for i in range(len(X_list)):
        X_list[i], Y_list[i], Z_list[i] = rotate_surface(X_list[i], Y_list[i], Z_list[i], axis, angle)
    update_plot(X_list, Y_list, Z_list)


# Создание основного окна
window = tk.Tk()
window.title("Билинейная поверхность")

# Фреймы для организации интерфейса
frame_left = tk.Frame(window)
frame_left.pack(side=tk.LEFT, padx=10)

frame_right = tk.Frame(window)
frame_right.pack(side=tk.LEFT, padx=10)

# Поля ввода для координат (левая часть)
labels = ["Point 1 (x1,y1,z1)", "Point 2 (x2,y2,z2)", "Point 3 (x3,y3,z3)", "Point 4 (x4,y4,z4)"]
entries = []

for label in labels:
    tk.Label(frame_left, text=label).pack()
    entry = tk.Entry(frame_left)
    entry.pack()
    entries.append(entry)

(entry_point1, entry_point2, entry_point3, entry_point4) = entries

# Кнопка для первичной отрисовки
draw_button = tk.Button(frame_left, text="Отрисовать", command=on_draw)
draw_button.pack(pady=5)

# Поля ввода для поворота (правая часть)
label_axis = tk.Label(frame_right, text="Ось (X/Y):")
label_axis.pack()
entry_axis = tk.Entry(frame_right)
entry_axis.pack()

label_angle = tk.Label(frame_right, text="Угол (градусы):")
label_angle.pack()
entry_angle = tk.Entry(frame_right)
entry_angle.pack()

# Кнопка для поворота
rotate_button = tk.Button(frame_right, text="Rotate", command=on_rotate)
rotate_button.pack(pady=5)

# Списки для хранения координат всех поверхностей
X_list = []
Y_list = []
Z_list = []

# Запуск основного цикла приложения
window.mainloop()
