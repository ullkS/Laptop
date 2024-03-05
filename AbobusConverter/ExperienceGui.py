from tkinter import filedialog, Canvas, VERTICAL, LEFT
import cv2
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def load_image():
    global img, img_label, img_original_label, image_path, original_img
    file_path = filedialog.askopenfilename()
    image_path = file_path
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    original_img = img.copy()
    img = cv2.resize(img, (500, 500))
    original_img = cv2.resize(original_img, (500, 500))
    display_image(img, img_label)
    display_image(original_img, img_original_label)

def display_image(img, label):
    img_tk = ImageTk.PhotoImage(Image.fromarray(img))
    label.config(image=img_tk)
    label.image = img_tk

def convert_color(color_space):
    global img
    if img is not None:
        converted_img = cv2.cvtColor(img, color_space)
        display_image(converted_img, img_label)
    else:
        info_label.config(text="Ошибка. Загрузите другое изображение.")

def get_image_info():
    global img
    if img is not None and img.size > 0:
        global image_path
        img = cv2.imread(image_path)
        file_size = os.path.getsize(image_path)
        file_format = os.path.splitext(image_path)[1]
        file_name = os.path.basename(image_path)
        color_model = "BGR"
        info = f"Имя файла: {file_name}\nРазмер файла: {file_size}\nЦветовая модель: {color_model}\nФормат файла: {file_format}\nРазмер изображения: {img.shape}\nТип данных: {img.dtype}\nКоличество каналов: {img.shape[2]}\nМинимальное значение пикселя: {img.min()}\nМаксимальное значение пикселя: {img.max()}"
        info_label.config(text=info)
    else:
        print("Не удалось загрузить изображение.")
        return

def clear_info():
    info_label.config(text="")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Abobus Converter")
root.attributes('-fullscreen', True)  # Открывает приложение на весь экран
img = None
image_path = ""
original_img = None

load_button = tk.Button(root, text="Загрузить изображение", command=load_image)
load_button.pack(pady=10)

canvas = Canvas(root, width=1000, height=500, scrollregion=(0, 0, 1000, 500))
canvas.pack(side=LEFT)

scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.config(yscrollcommand=scrollbar.set)
img_frame = tk.Frame(canvas)
canvas.create_window(0, 0, anchor=tk.NW, window=img_frame)

img_label = tk.Label(img_frame)
img_label.pack(side=tk.LEFT)

img_original_label = tk.Label(img_frame)
img_original_label.pack(side=tk.LEFT)

color_spaces = {
    'RGB': cv2.COLOR_BGR2RGB,
    'LAB': cv2.COLOR_BGR2LAB,
    'HSV': cv2.COLOR_BGR2HSV,
    'YCrCb': cv2.COLOR_BGR2YCrCb
}

info_button = tk.Button(root, text="Информация о изображении", command=get_image_info)
info_button.pack(pady=10)

clear_button = tk.Button(root, text="Очистить информацию", command=clear_info)
clear_button.pack(pady=10)

color_space_combo = ttk.Combobox(root, values=list(color_spaces.keys()))
color_space_combo.pack(pady=10)
color_space_combo.current(0)

convert_button = tk.Button(root, text="Конвертация цвета", command=lambda: convert_color(color_spaces[color_space_combo.get()]))
convert_button.pack(pady=10)

exit_button = tk.Button(root, text="Выход", command=exit_app)
exit_button.pack(pady=10)

info_label = tk.Label(root, text="")
info_label.pack()

root.mainloop()