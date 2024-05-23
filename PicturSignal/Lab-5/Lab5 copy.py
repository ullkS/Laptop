import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.image = None
        self.defimg = None

        self.load_button = tk.Button(self.root, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()

        self.nonlinear_correction_button = tk.Button(root, text="Дефолтные настройки", command=self.defoult_image)
        self.nonlinear_correction_button.pack()

        self.process_buttons_frame = tk.Frame(self.root)
        self.process_buttons_frame.pack()

        self.erode_button = tk.Button(self.process_buttons_frame, text="Харриса", command=self.erode_image)
        self.erode_button.pack(side=tk.LEFT)

        self.dilate_button = tk.Button(self.process_buttons_frame, text="SIFT", command=self.dilate_image)
        self.dilate_button.pack(side=tk.LEFT)

        self.opening_button = tk.Button(self.process_buttons_frame, text="SURF", command=self.opening_image)
        self.opening_button.pack(side=tk.LEFT)

        self.closing_button = tk.Button(self.process_buttons_frame, text="FAST", command=self.closing_image)
        self.closing_button.pack(side=tk.LEFT)

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.defimg = self.image
            self.display_image(self.image)

    def display_image(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400, 300))
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def defoult_image(self):
        self.image = self.defimg
        self.display_image(self.image)

    def erode_image(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((5,5), np.uint8)
            image = cv2.erode(gray, kernel, iterations=1)
            self.display_image(image)

    def dilate_image(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((5,5), np.uint8)
            image = cv2.dilate(gray, kernel, iterations=1)
            self.display_image(image)

    def opening_image(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((5,5), np.uint8)
            image = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
            self.display_image(image)

    def closing_image(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((5,5), np.uint8)
            image = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
            self.display_image(image)

    def gradient_image(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((5,5), np.uint8)
            image = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
            self.display_image(image)

def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()