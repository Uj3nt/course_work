import tkinter as tk
from tkinter import ttk, messagebox
from database import create_order  # Импортируем функцию создания заказа


def create_order_window():
    def fetch_clients():
        """Получение списка клиентов из базы данных."""
        import sqlite3
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ClientID, FirstName, LastName FROM Clients")
        clients = cursor.fetchall()
        conn.close()
        return clients

    def fetch_cars(client_id):
        """Получение автомобилей клиента из базы данных."""
        import sqlite3
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT CarID, Make, Year FROM Cars WHERE ClientID = ?", (client_id,))
        cars = cursor.fetchall()
        conn.close()
        return cars

    def fetch_services():
        """Получение списка услуг из базы данных."""
        import sqlite3
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

    def save_order():
        """Сохранение заказа в базу данных."""
        try:
            selected_client_id = int(clients_combobox.get().split(":")[0])
            selected_car_id = int(cars_combobox.get().split(":")[0])
            selected_service_ids = [int(service_listbox.get(idx).split(":")[0])
                                    for idx in service_listbox.curselection()]
            if not selected_service_ids:
                raise ValueError("Не выбраны услуги.")

            # Создание заказа через функцию работы с базой
            create_order(selected_car_id, selected_service_ids)
            messagebox.showinfo("Успех", "Заказ успешно создан.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    window = tk.Tk()
    window.title("Создать заказ")

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

    # Выбор услуг
    tk.Label(window, text="Выберите услуги:").grid(row=2, column=0, padx=10, pady=5)
    services = fetch_services()
    service_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, height=10)
    for service in services:
        service_listbox.insert(tk.END, f"{service[0]}: {service[1]} ({service[2]} руб.)")
    service_listbox.grid(row=2, column=1, padx=10, pady=5)

    # Кнопка сохранения
    save_button = tk.Button(window, text="Сохранить заказ", command=save_order)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

    window.mainloop()
