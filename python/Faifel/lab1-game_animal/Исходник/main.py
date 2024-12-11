import pickle
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

class Node:
    def __init__(self, data=None, yes=None, no=None):
        self.data = data
        self.yes = yes
        self.no = no

    def __str__(self):
        return str(self.data)

def save_tree(node, filename='animal_tree.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(node, f)

def load_tree(filename='animal_tree.pkl'):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return None

def AddNewAnimal(node):
    animal = simpledialog.askstring("Новое животное", "Введите задуманное животное:")
    question = simpledialog.askstring("Новый вопрос", "Введите вопрос, положительный ответ на который характерен для задуманного животного:")
    node.data = question
    node.yes = Node(animal)

def CheckAnimal(node):
    if node.yes is None and node.no is None: 
        user_input = messagebox.askquestion("Вопрос", f"Это {node}?")
        if user_input == 'yes':
            return
        else:
            node.no = Node(node.data)
            AddNewAnimal(node)
            return

    if node.yes is not None:
        user_input = messagebox.askquestion("Вопрос", f"{str(node)}?")
        if user_input == 'yes':
            CheckAnimal(node.yes)
        else:
            if node.no is None:
                node.no = Node() 
                AddNewAnimal(node.no)
            else:
                CheckAnimal(node.no)

def start_game():
    global root
    root.withdraw()  # Скрываем основное окно
    root = load_tree()
    if root is None:
        root = Node("Это животное большое?")
        root.yes = Node("Слон")
        root.no = Node("Мышь")

    while True:
        CheckAnimal(root)
        save_tree(root)
        if messagebox.askquestion("Продолжить игру", "Продолжить игру?") == 'no':
            break

    root.destroy()  

# Создание основного окна
root = tk.Tk()
root.title("Угадай животное")
root.geometry("280x150")

start_button = tk.Button(root, text="Начать игру", command=start_game)
start_button.pack(pady=20)

exit_button = tk.Button(root, text="Выход", command=root.quit)
exit_button.pack(pady=20)

root.mainloop()