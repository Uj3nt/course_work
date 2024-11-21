import tkinter as tk
from tkinter import ttk, messagebox
from database import add_car

def add_car_window():
    def fetch_clients():
        """Получение списка клиентов из базы данных."""
        import sqlite3
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ClientID, FirstName, LastName FROM Clients")
        clients = cursor.fetchall()
        conn.close()
        return clients

    def save_car():
        """Сохранение автомобиля в базу данных."""
        try:
            selected_client_id = int(clients_combobox.get().split(":")[0])
            make = entry_make.get()
            year = entry_year.get()
            vin = entry_vin.get()

            if not make or not year or not vin:
                raise ValueError("Заполните все поля!")

            # Проверка на корректный ввод года выпуска
            if not year.isdigit() or int(year) < 1900 or int(year) > 2100:
                raise ValueError("Введите корректный год выпуска!")

            # Сохранение автомобиля
            add_car(selected_client_id, make, int(year), vin)
            messagebox.showinfo("Успех", "Автомобиль успешно добавлен.")
            window.destroy()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    # Создание окна
    window = tk.Tk()
    window.title("Добавить автомобиль")

    # Выбор клиента
    tk.Label(window, text="Выберите клиента:").grid(row=0, column=0, padx=10, pady=5)
    clients = fetch_clients()
    clients_combobox = ttk.Combobox(window, values=[f"{client[0]}: {client[1]} {client[2]}" for client in clients])
    clients_combobox.grid(row=0, column=1, padx=10, pady=5)

    # Поля для ввода данных автомобиля
    tk.Label(window, text="Марка автомобиля:").grid(row=1, column=0, padx=10, pady=5)
    entry_make = tk.Entry(window)
    entry_make.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Год выпуска:").grid(row=2, column=0, padx=10, pady=5)
    entry_year = tk.Entry(window)
    entry_year.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(window, text="VIN:").grid(row=3, column=0, padx=10, pady=5)
    entry_vin = tk.Entry(window)
    entry_vin.grid(row=3, column=1, padx=10, pady=5)

    # Кнопка сохранения
    save_button = tk.Button(window, text="Сохранить", command=save_car)
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

    window.mainloop()
