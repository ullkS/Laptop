import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def load_image():
    global file_path, image
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_tk = ImageTk.PhotoImage(Image.fromarray(image))
        image_label.config(image=image_tk)
        image_label.image = image_tk

def reset_image():
    global file_path, image
    if file_path:
        image = cv2.imread(file_path)  # Load the original image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_tk = ImageTk.PhotoImage(Image.fromarray(image))
        image_label.config(image=image_tk)
        image_label.image = image_tk

def enhance_sharpness():
    sharpened_image = cv2.GaussianBlur(image, (5, 5), 0)
    sharpened_image = cv2.addWeighted(image, 1.5, sharpened_image, -0.5, 0)
    image_tk = ImageTk.PhotoImage(Image.fromarray(sharpened_image))
    image_label.config(image=image_tk)
    image_label.image = image_tk

def apply_blur():
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
    image_tk = ImageTk.PhotoImage(Image.fromarray(blurred_image))
    image_label.config(image=image_tk)
    image_label.image = image_tk

def apply_median_filter():
    median_filtered_image = cv2.medianBlur(image, 15)
    image_tk = ImageTk.PhotoImage(Image.fromarray(median_filtered_image))
    image_label.config(image=image_tk)
    image_label.image = image_tk

def apply_canny_edge_detection():
    edges = cv2.Canny(image, 100, 200)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    image_tk = ImageTk.PhotoImage(Image.fromarray(edges_rgb))
    image_label.config(image=image_tk)
    image_label.image = image_tk

def apply_roberts_edge_detection():
    img = cv2.imread(file_path, cv2.COLOR_BGR2GRAY)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernelx = np.array([[-1, 0], [0, 1]], dtype=int)
    kernely = np.array([[0, -1], [1, 0]], dtype=int)
    x = cv2.filter2D(grayImage, cv2.CV_16S, kernelx)
    y = cv2.filter2D(grayImage, cv2.CV_16S, kernely)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Roberts = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    images = [rgb_img, Roberts]
    for i in range(2):
        image_tk = ImageTk.PhotoImage(Image.fromarray(images[i]))
        image_label.config(image=image_tk)
        image_label.image = image_tk
    plt.show()

root = tk.Tk()
root.title("Приложение для обработки изображений")

image_label = tk.Label(root)
image_label.pack()

load_button = tk.Button(root, text="Загрузка изображений", command=load_image)
load_button.pack()

reset_button = tk.Button(root, text="Сброс", command=reset_image)
reset_button.pack()

enhance_button = tk.Button(root, text="Повышение резкости", command=enhance_sharpness)
enhance_button.pack()

blur_button = tk.Button(root, text="Применить размытие в движении", command=apply_blur)
blur_button.pack()

median_button = tk.Button(root, text="Применить медианный фильтр", command=apply_median_filter)
median_button.pack()

canny_button = tk.Button(root, text="Точное обнаружение краев Canny", command=apply_canny_edge_detection)
canny_button.pack()

roberts_button = tk.Button(root, text="Обнаружение границ Робертса", command=apply_roberts_edge_detection)
roberts_button.pack()

root.mainloop()