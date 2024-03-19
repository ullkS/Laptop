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
        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.display_image(self.image)
    
    def display_image(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400, 300))
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img)
        self.display_label.config(image=img_tk)
        self.display_label.image = img_tk
        
    def adjust_image(self, event=None):
        brightness = self.brightness_scale.get()
        contrast = self.contrast_scale.get()
        
        adjusted_image = np.int16(self.image) * (contrast/127 + 1) - contrast + brightness
        adjusted_image = np.clip(adjusted_image, 0, 255)
        adjusted_image = np.uint8(adjusted_image)
        
        self.display_image(adjusted_image)
        
    def plot_histograms(self):
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            histogram = cv2.calcHist([self.image], [i], None, [256], [0, 256])
            plt.plot(histogram, color=color)
        plt.title('Histograms for Color Image')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()