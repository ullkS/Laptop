import tkinter as tk
from tkinter import messagebox
from sympy import symbols, sympify, to_dnf, to_cnf, Symbol
from sympy.logic.boolalg import truth_table
from itertools import product

def evaluate_expression():
    logical_expression = entry.get()
    try:
        # Заменяем 0 и 1 на False и True соответственно
        logical_expression = logical_expression.replace('0', 'False').replace('1', 'True')
        
        # Создаем символы для всех буквенных переменных
        variables = [Symbol(v) for v in set(logical_expression) if v.isalpha()]
        
        # Преобразуем введенное выражение в SymPy выражение
        expr = sympify(logical_expression)
        
        # Создаем таблицу истинности
        tt = list(truth_table(expr, variables))
        
        # Формируем строку таблицы истинности
        header = ' | '.join(str(var) for var in variables) + ' | Res'
        truth_table_str = header + '\n' + '-' * len(header) + '\n'
        for inputs in product([False, True], repeat=len(variables)):
            result = expr.subs(dict(zip(variables, inputs)))
            row = ' | '.join('1' if val else '0' for val in inputs) + f' | {"1" if result else "0"}'
            truth_table_str += row + '\n'
        
        # Определяем, истинно ли выражение в целом
        is_true = any(expr.subs(dict(zip(variables, inputs))) for inputs in product([False, True], repeat=len(variables)))
        overall_result = "Истинно" if is_true else "Ложно"
        
        # Получаем ДНФ и КНФ
        dnf_result = str(to_dnf(expr))
        cnf_result = str(to_cnf(expr))

        if dnf_result == 'False' and cnf_result == 'True':
            result_text.set(
                f"Результат: {overall_result}\n\n"
                f"КНФ и ДНФ не существует"
            )
        else:
            result_text.set(
                f"Таблица истинности:\n{truth_table_str}\n"
                f"Дизъюнктивная нормальная форма:\n{dnf_result}\n\n"
                f"Конъюнктивная нормальная форма:\n{cnf_result}\n\n"
                f"Результат: {overall_result}"
            )
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при обработке выражения: {e}")

def insert_operator(operator):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + operator)

def create_gui():
    global entry, result_text

    root = tk.Tk()
    root.title("Логический калькулятор")

    font = ("Arial", 12)

    tk.Label(root, text="Введите логическое выражение:", font=font).pack(pady=5)
    entry = tk.Entry(root, width=50, font=font)
    entry.pack(pady=5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="∧ (AND)", command=lambda: insert_operator('&'), font=font).pack(side=tk.LEFT, padx=2)
    tk.Button(button_frame, text="∨ (OR)", command=lambda: insert_operator('|'), font=font).pack(side=tk.LEFT, padx=2)
    tk.Button(button_frame, text="¬ (NOT)", command=lambda: insert_operator('~'), font=font).pack(side=tk.LEFT, padx=2)
    tk.Button(button_frame, text="→ (IMPLIES)", command=lambda: insert_operator('>>'), font=font).pack(side=tk.LEFT, padx=2)
    tk.Button(button_frame, text="↔ (EQUIV)", command=lambda: insert_operator('<<'), font=font).pack(side=tk.LEFT, padx=2)

    tk.Button(root, text="Вычислить", command=evaluate_expression, font=font).pack(pady=5)

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT, font=font)
    result_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()