import tkinter as tk
from tkinter import ttk, messagebox
import requests


# --- Логика бэкенда (API) ---
def convert():
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число!")
        return

    from_curr = combo_from.get()
    to_curr = combo_to.get()

    # Запрос к бесплатному API (курсы к USD)
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url).json()
        rates = response['rates']

        # Конвертация: сначала в USD, потом в нужную валюту
        usd_amount = amount / rates[from_curr]
        result = usd_amount * rates[to_curr]

        label_result.config(text=f"{result:.2f} {to_curr}")
    except Exception as e:
        messagebox.showerror("Ошибка", "Не удалось получить курс валют.")


# --- Логика фронтенда (GUI) ---
root = tk.Tk()
root.title("Конвертер валют")
root.geometry("300x250")

# Виджеты
tk.Label(root, text="Сумма:").pack(pady=5)
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Label(root, text="Из валюты:").pack(pady=5)
currencies = ["USD", "EUR", "RUB", "GBP", "KZT", "TRY"]
combo_from = ttk.Combobox(root, values=currencies, state="readonly")
combo_from.set("USD")  # По умолчанию
combo_from.pack()

tk.Label(root, text="В валюту:").pack(pady=5)
combo_to = ttk.Combobox(root, values=currencies, state="readonly")
combo_to.set("EUR")  # По умолчанию
combo_to.pack()

# Кнопка (Событие клика привязано к функции convert)
tk.Button(root, text="Конвертировать", command=convert, bg="lightgreen").pack(pady=10)

# Результат
label_result = tk.Label(root, text="0.00", font=("Arial", 14, "bold"))
label_result.pack()

root.mainloop()  # Запуск главного цикла окна