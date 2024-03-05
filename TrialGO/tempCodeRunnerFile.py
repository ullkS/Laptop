import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def convert_bgr_to_rgb(image):
    b, g, r = cv2.split(image)
    return cv2.merge([r, g, b])

def load_image():
    file_path = filedialog.askopenfilename()
    image = cv2.imread(file_path)
    image_rgb = convert_bgr_to_rgb(image)
    display_image(image_rgb)

def display_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image)
    img_label.config(image=image_tk)
    img_label.image = image_tk

root = tk.Tk()
root.title("BGR to RGB Converter")

load_button = tk.Button(root, text="Загрузить изображение", command=load_image)
load_button.pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

root.mainloop()