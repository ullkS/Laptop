import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor App")
        self.image = None
        self.image_gray = None
        
        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()
        
        self.display_label = tk.Label(root)
        self.display_label.pack()
        
        self.brightness_scale = tk.Scale(root, label="Яркость", from_=-100, to=100, orient=tk.HORIZONTAL, command=self.adjust_image)
        self.brightness_scale.pack()
        
        self.contrast_scale = tk.Scale(root, label="Контрастность", from_=-100, to=100, orient=tk.HORIZONTAL, command=self.adjust_image)
        self.contrast_scale.pack()
        
        self.histogram_button = tk.Button(root, text="Построить гистограммы", command=self.plot_histograms)
        self.histogram_button.pack()
        
        self.gray_button = tk.Button(root, text="Преобразовать в градации серого", command=self.convert_to_gray)
        self.gray_button.pack()
        
        self.linear_correction_button = tk.Button(root, text="Линейная коррекция", command=self.linear_correction)
        self.linear_correction_button.pack()
        
        self.nonlinear_correction_button = tk.Button(root, text="Нелинейная коррекция", command=self.nonlinear_correction)
        self.nonlinear_correction_button.pack()

        self.nonlinear_correction_button = tk.Button(root, text="Дефолтные настройки", command=self.defoult_image)
        self.nonlinear_correction_button.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.imgUpdate = self.image
            self.image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.display_image(self.image)

    def display_image(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400, 300))
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img)
        self.display_label.config(image=img_tk)
        self.display_label.image = img_tk
    
    def defoult_image(self):
        self.imgupdate = self.image
        self.display_image(self.imgupdate)

    def adjust_image(self, event=None):
        brightness = self.brightness_scale.get()
        contrast = self.contrast_scale.get()
        adjusted_image = np.int16(self.image) * (contrast/127 + 1) - contrast + brightness
        adjusted_image = np.clip(adjusted_image, 0, 255)
        adjusted_image = np.uint8(adjusted_image)
        self.display_image(adjusted_image)
        self.imgUpdate = adjusted_image

    def plot_histograms(self):
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            histogram = cv2.calcHist([self.imgUpdate], [i], None, [256], [0, 256])
            plt.plot(histogram, color=color)
        plt.title('Histograms for Color Image')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.show()

    def convert_to_gray(self):
        self.display_image(self.image_gray)

    def linear_correction(self):
        linear_corrected_image = cv2.equalizeHist(self.image_gray)
        self.display_image(linear_corrected_image)

    def nonlinear_correction(self):
        nonlinear_corrected_image = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(self.image_gray)
        self.display_image(nonlinear_corrected_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()