from tkinter import filedialog
import cv2
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def load_image():
    global img, img_label, image_path
    file_path = filedialog.askopenfilename()
    image_path = file_path
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (500, 500))
    display_image(img)

def display_image(img):
    img_tk = ImageTk.PhotoImage(Image.fromarray(img))
    img_label.config(image=img_tk)
    img_label.image = img_tk

def convert_color(color_space):
    global img
    if img is not None:
        converted_img = cv2.cvtColor(img, color_space)
        display_image(converted_img)
    else:
        info_label.config(text="Ошибка.Загрузите другое изображение.")

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
    

root = tk.Tk()
root.title("Abobus Converter")
img = None
image_path = ""

load_button = tk.Button(root, text="Загрузить изображение", command=load_image)
load_button.pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

color_spaces = {
    'RGB': cv2.COLOR_BGR2RGB,
    'LAB': cv2.COLOR_BGR2LAB,
    'HSV': cv2.COLOR_BGR2HSV,
    'YCrCb': cv2.COLOR_BGR2YCrCb
}

info_button = tk.Button(root, text="Информация о изображении", command=get_image_info)
info_button.pack(pady=10)

color_space_combo = ttk.Combobox(root, values=list(color_spaces.keys()))
color_space_combo.pack(pady=10)
color_space_combo.current(0)

convert_button = tk.Button(root, text="конвертация цвета", command=lambda: convert_color(color_spaces[color_space_combo.get()]))
convert_button.pack(pady=10)

info_label = tk.Label(root, text="")
info_label.pack()

root.mainloop()