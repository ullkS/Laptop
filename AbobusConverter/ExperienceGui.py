from tkinter import filedialog, Canvas, VERTICAL, LEFT
import cv2
import os
import tkinter as tk
import numpy as np
from tkinter import ttk
from PIL import Image, ImageTk


def load_image():
    global img, img_label, img_original_label, image_path, original_img, flag, rgb_img, img_bgr
    file_path = filedialog.askopenfilename()
    image_path = file_path
    img = cv2.imread(file_path)
    img = cv2.resize(img, (500, 500))
    img_bgr = img.copy()
    rgb_img = bgr_to_rgb(img)  # Конвертация из BGR в RGB с помощью формул
    original_img = rgb_img.copy()
    img = rgb_img.copy()
    original_img = cv2.resize(original_img, (500, 500))
    flag = "RGB"
    display_image(img, img_label)
    display_image(original_img, img_original_label)

def display_image(img, label):
    img_tk = ImageTk.PhotoImage(Image.fromarray(img))
    label.config(image=img_tk)
    label.image = img_tk

def bgr_to_hsv(img_bgr):
    img = img_bgr.astype(np.float32) / 255.0
    R, G, B = img[..., 0], img[..., 1], img[..., 2]
    Cmax = np.max(img, axis=2)
    Cmin = np.min(img, axis=2)
    delta = Cmax - Cmin
    
    V = Cmax
    S = np.where(Cmax!= 0, delta / Cmax, 0)
    H = np.zeros_like(V)
    
    mask = (Cmax == R)
    H[mask] = 60 * ((G[mask] - B[mask]) / delta[mask] % 6)
    mask = (Cmax == G)
    H[mask] = 120 + 60 * ((B[mask] - R[mask]) / delta[mask] + 2)
    mask = (Cmax == B)
    H[mask] = 240 + 60 * ((R[mask] - G[mask]) / delta[mask] + 4)
    hsv_img = (np.dstack((H, S, V)) * 255).astype(np.uint8)
    return hsv_img

def bgr_to_xyz(img_bgr):
    img = img_bgr.astype(np.float32) / 255.0
    R, G, B = img[..., 0], img[..., 1], img[..., 2]
    X = 0.412453*R + 0.357580*G + 0.189423*B
    Y = 0.212671*R + 0.715160*G + 0.072169*B 
    Z = 0.019334*R + 0.119193*G + 0.950227*B
    xyz_img = (np.dstack((X,Y,Z)) * 255).astype(np.uint8)
    return xyz_img

def bgr_to_cmyk(img_bgr):
    img = img_bgr.astype(np.float64)/255
    K = 1 - np.max(img, axis=2)
    C = (1-img[...,2] - K)/(1-K)
    M = (1-img[...,1] - K)/(1-K)
    Y = (1-img[...,0] - K)/(1-K)

    image = (np.dstack((C,M,Y,K)) * 255).astype(np.uint8)
    return image


def bgr_to_lab(img_bgr):
    img = img_bgr.astype(np.float32) / 255.0
    R, G, B = img[..., 0], img[..., 1], img[..., 2]

    X = 0.412453*R + 0.357580*G + 0.189423*B
    Y = 0.212671*R + 0.715160*G + 0.072169*B 
    Z = 0.019334*R + 0.119193*G + 0.950227*B

    Xo = 244.66128
    Yo = 255.0
    Zo = 277.63227

    L = 116 * (Y / Yo) - 16
    a = 500 * ((X / Xo) - (Y / Yo))
    b = 200 * ((Y / Yo) - (Z / Zo))
    lab_img = (np.dstack((L,a,b)) * 255).astype(np.uint8)
    return lab_img
    

def bgr_to_hsl(img_bgr):
    img = img_bgr.astype(np.float32) / 255.0
    R, G, B = img[..., 0], img[..., 1], img[..., 2]
      
    Cmax = np.max(img, axis=2)
    Cmin = np.min(img, axis=2)
    delta = Cmax - Cmin
      
    H = np.zeros_like(delta)
    S = np.zeros_like(delta)
    L = (Cmax + Cmin)/2


    H[Cmax == R] = 60 * (((G - B)/delta)[Cmax == R] % 6)
    H[Cmax == G] = 120 + 60 * (((B - R)/delta)[Cmax == G] + 2)
    H[Cmax == B] = 240 + 60 * (((R - G)/delta)[Cmax == B] + 4)

    S[delta != 0] = delta[delta != 0] / (1 - np.abs(2 * L[delta != 0] - 1))
      
    image = (np.dstack((H,S,L)) * 255).astype(np.uint8)
    return image


def rgb_to_ycbcr(imf_ycbcr):
    img = imf_ycbcr.astype(np.float32) / 255.0
    R, G, B = img[..., 0], img[..., 1], img[..., 2]
      
    Cmax = np.max(img, axis=2)
    Cmin = np.min(img, axis=2)  
      
    Y = (Cmax + Cmin) / 2
    C = (Cmax - R) / (1 - np.abs(2 * Y - 1))
    B = (Cmax - G) / (1 - np.abs(2 * Y - 1))
    
    image = (np.dstack((Y,C,B)) * 255).astype(np.uint8)
    return image  

def bgr_to_rgb(img):
    h, w, _ = img.shape
    rgb_img = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            b, g, r = img[i, j]
            rgb_img[i, j] = [r, g, b]
    return rgb_img

def convert_color(color_space):
    global img, original_img, img_bgr, flag
    if img is not None:
        if color_space == 'RGB':
            flag = 'RGB'
            converted_img = original_img.copy()
        elif color_space == 'HSV':
            flag = 'HSV'
            converted_img = bgr_to_hsv(img_bgr) 
        elif color_space == 'BGR':  
            flag = 'BGR'
            converted_img = img_bgr.copy()  
        elif color_space == 'HSL':  
            flag = 'HSL'
            converted_img = bgr_to_hsl(img_bgr)    
        elif color_space == 'CMYK':  
            flag = 'CMYK'
            converted_img = bgr_to_cmyk(img_bgr) 
        elif color_space == 'YCBCR':
            flag = 'YCBCR'
            converted_img = rgb_to_ycbcr(img_bgr)
        elif color_space == 'LAB':
            flag = 'LAB'
            converted_img = bgr_to_lab(img_bgr)
        elif color_space == 'XYZ':
            flag = 'XYZ'
            converted_img = bgr_to_xyz(img_bgr)
        display_image(converted_img, img_label)
    else:
        info_label.config(text="Ошибка. Загрузите другое изображение.")

def get_image_info():
    if img is not None and img.size > 0:
        global image_path
        imgg = cv2.imread(image_path)
        file_size = os.path.getsize(image_path)
        file_format = os.path.splitext(image_path)[1]
        file_name = os.path.basename(image_path)
        info = f"Имя файла: {file_name}\nРазмер файла: {file_size}\nЦветовая модель: {flag}\nФормат файла: {file_format}\nРазмер изображения: {imgg.shape}\nТип данных: {imgg.dtype}\nКоличество каналов: {imgg.shape[2]}\nМинимальное значение пикселя: {imgg.min()}\nМаксимальное значение пикселя: {imgg.max()}"
        info_label.config(text=info)
    else:
        print("Не удалось загрузить изображение.")
        return

def clear_info():
    info_label.config(text="")

def exit_app():
    root.destroy()

color_spaces = {
    'BGR': 'BGR',
    'RGB': 'RGB',
    'HSV': 'HSV',
    'HSL': 'HSL',
    'CMYK': 'CMYK',
    'YCBCR': 'YCBCR',
    'LAB': 'LAB',
    'XYZ': 'XYZ',
}

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
img_original_label = tk.Label(img_frame)
img_original_label.pack(side=tk.LEFT)
img_label = tk.Label(img_frame)
img_label.pack(side=tk.LEFT)

info_button = tk.Button(root, text="Информация о изображении", command=get_image_info)
info_button.pack(pady=10)

clear_button = tk.Button(root, text="Очистить информацию", command=clear_info)
clear_button.pack(pady=10)

color_space_combo = ttk.Combobox(root, values=list(color_spaces.keys()))
color_space_combo.pack(pady=10)
color_space_combo.current(0)

convert_button = tk.Button(root, text="Конвертация цвета", command=lambda: convert_color(color_space_combo.get()))
convert_button.pack(pady=10)

exit_button = tk.Button(root, text="Выход", command=exit_app)
exit_button.pack(pady=10)

info_label = tk.Label(root, text="")
info_label.pack()

root.mainloop()