from itertools import product
import tkinter as tk
from tkinter import messagebox

# Функция для проверки, является ли строка логической переменной
def is_variable(s):
    return s.isalpha() and len(s) == 1

# Функция для оценки логического выражения с заданным контекстом
def eval_expression(expr, context):
    # Заменяем переменные на их значения
    for var in context:
        expr = expr.replace(var, str(context[var]))
    # Выполняем вычисления
    expr = expr.replace('¬', ' not ')
    expr = expr.replace('∧', ' and ')
    expr = expr.replace('∨', ' or ')
    expr = expr.replace('→', ' <= ')  # Импликация: A → B = ¬A ∨ B
    expr = expr.replace('↔', ' == ')  # Эквиваленция: A ↔ B = (A → B) ∧ (B → A)
    return eval(expr)

# Функция для преобразования логического выражения в ДНФ
def to_dnf(expr):
    expr = expr.replace('AND', '∧').replace('OR', '∨').replace('NOT', '¬')
    variables = sorted(set(filter(is_variable, expr)))
    table = []

    for combination in product([False, True], repeat=len(variables)):
        context = dict(zip(variables, combination))
        truth_value = eval_expression(expr, context)
        table.append((combination, truth_value))

    return variables, table

# Функция для формирования ДНФ из таблицы истинности
def get_dnf(variables, table):
    dnf_terms = []
    for combination, value in table:
        if value:  # Извлекаем строки, где выражение истинно
            term = []
            for var, state in zip(variables, combination):
                if state:  # Если переменная истинна
                    term.append(var)
                else:  # Если переменная ложна
                    term.append(f'¬{var}')
            dnf_terms.append('(' + ' ∧ '.join(term) + ')')
    return ' ∨ '.join(dnf_terms)

# Функция для формирования КНФ из таблицы истинности
def get_knf(variables, table):
    knf_clauses = []
    for combination, value in table:
        if not value:  # Извлекаем строки, где выражение ложно
            clause = []
            for var, state in zip(variables, combination):
                if state:  # Если переменная истинна
                    clause.append(f'¬{var}')
                else:  # Если переменная ложна
                    clause.append(var)
            knf_clauses.append('(' + ' ∨ '.join(clause) + ')')
    return ' ∧ '.join(knf_clauses)

# Функция для формирования таблицы истинности
def print_truth_table(variables, table):
    header = ' | '.join(variables) + ' | Res'
    print(header)
    print('-' * len(header))
    for combination, truth_value in table:
        truth_row = ' | '.join(str(int(val)) for val in combination)
        print(f"{truth_row} | {int(truth_value)}")

def evaluate_expression():
    logical_expression = entry.get()
    try:
        variables, truth_table = to_dnf(logical_expression)
        
        # Создаем заголовок таблицы
        header = ' | '.join(variables) + ' | Res'
        # Формируем строки таблицы истинности
        truth_table_str = header + '\n' + '-' * len(header) + '\n'
        truth_table_str += "\n".join(
            f"{' | '.join(str(int(val)) for val in combination)} | {int(truth_value)}"
            for combination, truth_value in truth_table
        )
        
        # Определяем, истинно ли выражение в целом
        is_true = any(truth_value for _, truth_value in truth_table)
        overall_result = "Истинно" if is_true else "Ложно"
        
        dnf_result = get_dnf(variables, truth_table)
        knf_result = get_knf(variables, truth_table)

        if (not knf_result) or (not dnf_result):
            result_text.set(
                f"Результат: {overall_result}\n\n"
                f"КНФ и ДНФ не существует"
        )
        else:
            result_text.set(
                f"Таблица истинности:\n{truth_table_str}\n\n"
                f"Дизъюнктивная нормальная форма:\n{dnf_result}\n\n"
                f"Конъюнктивная нормальная форма:\n{knf_result}\n\n"
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

    # Set a font that supports Unicode
    font = ("Arial", 12)

    tk.Label(root, text="Введите логическое выражение:", font=font).pack(pady=5)
    entry = tk.Entry(root, width=50, font=font)
    entry.pack(pady=5)

    # Add buttons for logical operators
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="∧ (AND)", command=lambda: insert_operator('∧'), font=font).pack(side=tk.LEFT, padx=2)
    tk.Button(button_frame, text="∨ (OR)", command=lambda: insert_operator('∨'), font=font).pack(side=tk.LEFT, padx=2)
    tk.Button(button_frame, text="¬ (NOT)", command=lambda: insert_operator('¬'), font=font).pack(side=tk.LEFT, padx=2)
    tk.Button(button_frame, text="→ (IMPLIES)", command=lambda: insert_operator('→'), font=font).pack(side=tk.LEFT, padx=2)
    tk.Button(button_frame, text="↔ (EQUIV)", command=lambda: insert_operator('↔'), font=font).pack(side=tk.LEFT, padx=2)

    tk.Button(root, text="Вычислить", command=evaluate_expression, font=font).pack(pady=5)

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT, font=font)
    result_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()