import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Параметры окна
x_min, x_max, y_min, y_max = 1, 8, 1, 8


# Генерация случайных отрезков
def generate_segments(n):
    segments = []
    for _ in range(n):
        x1, y1 = random.uniform(0, 10), random.uniform(0, 10)
        x2, y2 = random.uniform(0, 10), random.uniform(0, 10)
        segments.append(((x1, y1), (x2, y2)))
    return segments


# Функция для вычисления кода региона
def compute_code(x, y):
    code = 0
    if y > y_max:
        code |= 8
    if y < y_min:
        code |= 4
    if x < x_min:
        code |= 2
    if x > x_max:
        code |= 1
    return code


# Алгоритм Коэна-Сазерленда
def cohen_sutherland_clip(x1, y1, x2, y2):
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    while True:
        if code1 == 0 and code2 == 0:
            return [(x1, y1), (x2, y2)]
        elif (code1 & code2) != 0:
            return None
        else:
            code_out = code1 if code1 != 0 else code2
            if code_out & 8:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & 4:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & 2:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min
            elif code_out & 1:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max

            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)


# Функция для отрисовки отрезков и окна
def draw_segments(highlight_clipped=False):
    ax.clear()
    ax.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min], color="black")

    for (x1, y1), (x2, y2) in segments:
        ax.plot([x1, x2], [y1, y2], color="blue")

    if highlight_clipped:
        for (x1, y1), (x2, y2) in segments:
            clipped = cohen_sutherland_clip(x1, y1, x2, y2)
            if clipped:
                (x1_clip, y1_clip), (x2_clip, y2_clip) = clipped
                ax.plot([x1_clip, x2_clip], [y1_clip, y2_clip], color="red")

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    canvas.draw()


# Функции для кнопок управления
def highlight_segments():
    draw_segments(highlight_clipped=True)


def new_segments():
    global segments
    segments = generate_segments(10)
    draw_segments()


def update_window():
    global x_min, x_max, y_min, y_max
    x_min = x_min_slider.get()
    x_max = x_max_slider.get()
    y_min = y_min_slider.get()
    y_max = y_max_slider.get()
    draw_segments()


# Создаем основное окно и фреймы для интерфейса
root = tk.Tk()
root.title("Отрезки с использованием окна Коэна-Сазерленда")

# Фрейм для настроек
control_frame = ttk.Frame(root)
control_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

# Поле для графика
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

segments = generate_segments(10)
draw_segments()

# Добавление кнопок и слайдеров
ttk.Button(control_frame, text="Выделить", command=highlight_segments).pack(pady=5)
ttk.Button(control_frame, text="Новые отрезки", command=new_segments).pack(pady=5)

# Настройка ползунков для изменения размеров окна
ttk.Label(control_frame, text="X Min").pack()
x_min_slider = ttk.Scale(control_frame, from_=0, to=10, orient='horizontal', command=lambda _: update_window())
x_min_slider.set(x_min)
x_min_slider.pack()

ttk.Label(control_frame, text="X Max").pack()
x_max_slider = ttk.Scale(control_frame, from_=0, to=10, orient='horizontal', command=lambda _: update_window())
x_max_slider.set(x_max)
x_max_slider.pack()

ttk.Label(control_frame, text="Y Min").pack()
y_min_slider = ttk.Scale(control_frame, from_=0, to=10, orient='horizontal', command=lambda _: update_window())
y_min_slider.set(y_min)
y_min_slider.pack()

ttk.Label(control_frame, text="Y Max").pack()
y_max_slider = ttk.Scale(control_frame, from_=0, to=10, orient='horizontal', command=lambda _: update_window())
y_max_slider.set(y_max)
y_max_slider.pack()

root.mainloop()
