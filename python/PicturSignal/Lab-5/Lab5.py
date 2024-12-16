import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class KeyPointsDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обнаружение ключевых точек")

        self.image = None
        self.original_image = None

        self.label = tk.Label(self.root)
        self.label.pack()

        self.btn_load_image = tk.Button(self.root, text="Загрузить изображение", command=self.load_image)
        self.btn_load_image.pack()

        self.btn_harris = tk.Button(self.root, text="Обнаружить Harris", command=self.detect_harris)
        self.btn_harris.pack(side=tk.LEFT)

        self.btn_sift = tk.Button(self.root, text="Обнаружить SIFT", command=self.detect_sift)
        self.btn_sift.pack(side=tk.LEFT)

        self.btn_fast = tk.Button(self.root, text="Обнаружить FAST", command=self.detect_fast)
        self.btn_fast.pack(side=tk.LEFT)
        
        self.btn_surf = tk.Button(self.root, text="Обнаружить SURF(ORB)", command=self.detect_surf)
        self.btn_surf.pack(side=tk.LEFT)

        self.btn_default = tk.Button(self.root, text="Изображение по умолчанию", command=self.display_default_image)
        self.btn_default.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.original_image = self.image.copy()
            self.display_image()

    def detect_harris(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            harris = cv2.cornerHarris(gray, 2, 3, 0.04)
            self.image[harris > 0.01 * harris.max()] = [0, 0, 255]  # Показать Harris-корни в красном цвете
            self.display_image()

    def detect_sift(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            sift = cv2.SIFT_create()
            keypoints, descriptors = sift.detectAndCompute(gray, None)
            image_sift = cv2.drawKeypoints(self.image, keypoints, None)
            self.display_image(image_sift)

    def detect_surf(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            surf = cv2.ORB_create()
            keypoints, descriptors = surf.detectAndCompute(gray, None)
            image_surf = cv2.drawKeypoints(self.image, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            self.display_image(image_surf)

    def detect_fast(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            fast = cv2.FastFeatureDetector_create()
            keypoints = fast.detect(gray, None)
            image_fast = cv2.drawKeypoints(self.image, keypoints, None)
            self.display_image(image_fast)

    def display_default_image(self):
        self.image = self.original_image.copy()
        self.display_image()

    def display_image(self, image=None):
        if image is None:
            image = self.image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image_tk = ImageTk.PhotoImage(image)
        self.label.configure(image=image_tk)
        self.label.image = image_tk

root = tk.Tk()
app = KeyPointsDetectorApp(root)
root.mainloop()