from itertools import product
import tkinter as tk
from tkinter import messagebox

def is_variable(s):
    return s.isalpha() and len(s) == 1

# Функция оценки логического выражения 
def eval_expression(expr, context):
    for var in context:
        expr = expr.replace(var, str(context[var]))
    # Мапа преобразований
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

# Функция для формирования ДНФ из ТИ
def get_dnf(variables, table):
    dnf_terms = []
    for combination, value in table:
        if value:  
            term = []
            for var, state in zip(variables, combination):
                if state:  
                    term.append(var)
                else:  
                    term.append(f'¬{var}')
            dnf_terms.append('(' + ' ∧ '.join(term) + ')')
    return ' ∨ '.join(dnf_terms)

# Функция для формирования КНФ из ТИ
def get_knf(variables, table):
    knf_clauses = []
    for combination, value in table:
        if not value:  
            clause = []
            for var, state in zip(variables, combination):
                if state:  # Если переменная истинна
                    clause.append(f'¬{var}')
                else:  # Если переменная ложна
                    clause.append(var)
            knf_clauses.append('(' + ' ∨ '.join(clause) + ')')
    return ' ∧ '.join(knf_clauses)

# Функция для формирования таблицы истинности(ТИ)
def print_truth_table(variables, table):
    header = ' | '.join(variables) + ' | Result'
    print(header)
    print('-' * len(header))
    for combination, truth_value in table:
        truth_row = ' | '.join(str(int(val)) for val in combination)
        print(f"{truth_row} | {int(truth_value)}")

def evaluate_expression():
    logical_expression = entry.get()
    try:
        variables, truth_table = to_dnf(logical_expression)

        header = ' | '.join(variables) + ' | Result'
        
        # Формирование строки ТИ
        truth_table_str = header + '\n' + '-' * len(header) + '\n'
        truth_table_str += "\n".join(
            f"{' | '.join(str(int(val)) for val in combination)} | {int(truth_value)}"
            for combination, truth_value in truth_table
        )
        
        dnf_result = get_dnf(variables, truth_table)
        knf_result = get_knf(variables, truth_table)

        result_text.set(
            f"Таблица истинности:\n{truth_table_str}\n\n"
            f"Дизъюнктивная нормальная форма (ДНФ):\n{dnf_result}\n\n"
            f"Конъюнктивная нормальная форма (КНФ):\n{knf_result}"
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

    # Поддержка Unicode string
    font = ("Arial", 12)

    tk.Label(root, text="Введите логическое выражение:", font=font).pack(pady=5)
    entry = tk.Entry(root, width=50, font=font)
    entry.pack(pady=5)

    # Buttons:)
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