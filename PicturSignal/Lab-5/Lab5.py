import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

image = None
video_capture = None

def load_image():
    global image
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        display_image(image)

def display_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (400, 300))
    img = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def detect_keypoints_harris(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners = cv2.cornerHarris(gray_image, 2, 3, 0.04)
    corners = np.int0(corners)
    for i in corners:
        x, y = i.ravel()
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    display_image(image)

def detect_keypoints_sift(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray_image, None)
    for keypoint in keypoints:
        x, y = keypoint.pt
        cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)
    display_image(image)

def detect_keypoints_surf(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    surf = cv2.xfeatures2d.SURF_create()
    keypoints, descriptors = surf.detectAndCompute(gray_image, None)
    for keypoint in keypoints:
        x, y = keypoint.pt
        cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)
    display_image(image)

def detect_keypoints_fast(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fast = cv2.FastFeatureDetector_create()
    keypoints = fast.detect(gray_image, None)
    for keypoint in keypoints:
        x, y = keypoint.pt
        cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)
    display_image(image)

def load_video():
    global video_capture
    file_path = filedialog.askopenfilename(title="Open Video", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if file_path:
        video_capture = cv2.VideoCapture(file_path)
        process_video()

def process_video():
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        display_image(frame)

root = tk.Tk()
root.title("Image and Video Processing")

image_label = tk.Label(root)
image_label.pack()

load_image_button = tk.Button(root, text="Load Image", command=load_image)
load_image_button.pack()

harris_button = tk.Button(root, text="Detect Keypoints (Harris)", command=lambda: detect_keypoints_harris(image))
harris_button.pack()

sift_button = tk.Button(root, text="Detect Keypoints (SIFT)", command=lambda: detect_keypoints_sift(image))
sift_button.pack()

surf_button = tk.Button(root, text="Detect Keypoints (SURF)", command=lambda: detect_keypoints_surf(image))
surf_button.pack()

fast_button = tk.Button(root, text="Detect Keypoints (FAST)", command=lambda: detect_keypoints_fast(image))
fast_button.pack()

load_video_button = tk.Button(root, text="Load Video", command=load_video)
load_video_button.pack()

root.mainloop()