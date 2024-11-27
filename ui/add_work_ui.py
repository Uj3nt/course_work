import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def add_work_window():
    def fetch_clients():
        """Получение списка клиентов из базы данных."""
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ClientID, FirstName, LastName FROM Clients")
        clients = cursor.fetchall()
        conn.close()
        return clients

    def fetch_cars(client_id):
        """Получение автомобилей клиента из базы данных."""
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT CarID, Make, Year FROM Cars WHERE ClientID = ?", (client_id,))
        cars = cursor.fetchall()
        conn.close()
        return cars

    def fetch_services():
        """Получение списка услуг из базы данных."""
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ServiceID, ServiceName, ServicePrice FROM Services")
        services = cursor.fetchall()
        conn.close()
        return services

    def update_cars(event):
        """Обновление списка автомобилей при выборе клиента."""
        selected_client_id = clients_combobox.get().split(":")[0]
        cars = fetch_cars(selected_client_id)
        cars_combobox['values'] = [f"{car[0]}: {car[1]} ({car[2]})" for car in cars]
        cars_combobox.set("")

    def add_service_to_check(service_id=None, service_name=None, service_price=None):
        """Добавить услугу в чек."""
        if not service_id:  # Для произвольной услуги
            service_name = entry_custom_service_name.get()
            service_price = entry_custom_service_price.get()
            if not service_name or not service_price:
                messagebox.showerror("Ошибка", "Заполните все поля для произвольной услуги!")
                return
            try:
                service_price = float(service_price)
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную стоимость!")
                return
        else:  # Для заранее заданной услуги
            try:
                service_price = float(service_price)  # Приведение цены к типу float
            except (ValueError, TypeError):
                messagebox.showerror("Ошибка", "Некорректная цена услуги!")
                return

        # Добавляем услугу в текущий чек
        current_check.append({"name": service_name, "price": service_price})
        refresh_check_list()

    def refresh_check_list():
        """Обновить отображение чека."""
        check_list.delete(*check_list.get_children())
        total = 0
        for idx, item in enumerate(current_check):
            check_list.insert("", "end", values=(idx + 1, item["name"], item["price"]))
            total += item["price"]
        total_label.config(text=f"Итого: {total} руб.")

    def save_check():
        """Сохранить чек в историю работ."""
        try:
            selected_car_id = int(cars_combobox.get().split(":")[0])
            total_cost = sum(item["price"] for item in current_check)
            if not current_check:
                raise ValueError("Чек пуст, добавьте услуги или позиции.")

            conn = sqlite3.connect('autoshop.db')
            cursor = conn.cursor()

            # Сохранение чека в историю работ
            for item in current_check:
                cursor.execute('''
                    INSERT INTO WorkHistory (OrderID, Date, Description, TotalCost)
                    VALUES (?, date('now'), ?, ?)
                ''', (selected_car_id, item["name"], item["price"]))

            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", f"Чек сохранён. Общая сумма: {total_cost} руб.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # Главное окно
    window = tk.Tk()
    window.title("Добавить работу (формирование чека)")
    window.geometry("960x680")

    # Выбор клиента
    tk.Label(window, text="Выберите клиента:").grid(row=0, column=0, padx=10, pady=5)
    clients = fetch_clients()
    clients_combobox = ttk.Combobox(window, values=[f"{client[0]}: {client[1]} {client[2]}" for client in clients])
    clients_combobox.grid(row=0, column=1, padx=10, pady=5)
    clients_combobox.bind("<<ComboboxSelected>>", update_cars)

    # Выбор автомобиля
    tk.Label(window, text="Выберите автомобиль:").grid(row=1, column=0, padx=10, pady=5)
    cars_combobox = ttk.Combobox(window)
    cars_combobox.grid(row=1, column=1, padx=10, pady=5)

    # Список доступных услуг
    tk.Label(window, text="Добавить услугу:").grid(row=2, column=0, padx=10, pady=5)
    services = fetch_services()
    services_listbox = tk.Listbox(window, height=10, width=70)
    for service in services:
        services_listbox.insert(tk.END, f"{service[0]}: {service[1]} ({service[2]} руб.)")
    services_listbox.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(window, text="Добавить выбранную услугу", command=lambda: add_service_to_check(
        *services_listbox.get(services_listbox.curselection()).split(":"),
        float(services_listbox.get(services_listbox.curselection()).split("(")[1].split(" руб")[0])
    )).grid(row=3, column=1, pady=5)

    # Добавление произвольной услуги
    tk.Label(window, text="Название произвольной услуги:").grid(row=4, column=0, padx=10, pady=5)
    entry_custom_service_name = tk.Entry(window)
    entry_custom_service_name.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(window, text="Стоимость:").grid(row=5, column=0, padx=10, pady=5)
    entry_custom_service_price = tk.Entry(window)
    entry_custom_service_price.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(window, text="Добавить позицию", command=lambda: add_service_to_check()).grid(row=6, column=1, pady=5)

    # Чек
    tk.Label(window, text="Чек:").grid(row=7, column=0, padx=10, pady=5)
    check_list = ttk.Treeview(window, columns=("№", "Описание", "Стоимость"), show="headings", height=10)
    check_list.heading("№", text="№")
    check_list.heading("Описание", text="Описание")
    check_list.heading("Стоимость", text="Стоимость")
    check_list.grid(row=7, column=1, padx=10, pady=5)

    total_label = tk.Label(window, text="Итого: 0 руб.")
    total_label.grid(row=8, column=1, padx=10, pady=5)

    # Сохранить чек
    tk.Button(window, text="Сохранить чек", command=save_check).grid(row=9, column=1, pady=10)

    # Локальные данные
    current_check = []

    window.mainloop()
