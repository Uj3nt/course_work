import tkinter as tk
from tkinter import ttk, messagebox
from database import add_client, add_car  # Импортируем функции для работы с клиентами и автомобилями

def manage_clients_window():
    def fetch_clients():
        """Получение всех клиентов из базы данных."""
        import sqlite3
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ClientID, FirstName, LastName, PhoneNumber FROM Clients")
        clients = cursor.fetchall()
        conn.close()
        return clients

    def refresh_client_list():
        """Обновить список клиентов."""
        client_list.delete(*client_list.get_children())  # Очистить текущий список
        for client in fetch_clients():
            client_list.insert("", "end", values=(client[0], client[1], client[2], client[3]))

    def open_add_client_window():
        """Открыть окно добавления клиента."""
        def save_client():
            first_name = entry_first_name.get()
            last_name = entry_last_name.get()
            phone = entry_phone.get()
            if first_name and last_name and phone:
                add_client(first_name, last_name, phone)
                messagebox.showinfo("Успех", "Клиент добавлен.")
                add_client_window.destroy()
                refresh_client_list()
            else:
                messagebox.showerror("Ошибка", "Заполните все поля!")

        # Окно добавления клиента
        add_client_window = tk.Toplevel(window)
        add_client_window.title("Добавить клиента")

        tk.Label(add_client_window, text="Имя").grid(row=0, column=0)
        entry_first_name = tk.Entry(add_client_window)
        entry_first_name.grid(row=0, column=1)

        tk.Label(add_client_window, text="Фамилия").grid(row=1, column=0)
        entry_last_name = tk.Entry(add_client_window)
        entry_last_name.grid(row=1, column=1)

        tk.Label(add_client_window, text="Телефон").grid(row=2, column=0)
        entry_phone = tk.Entry(add_client_window)
        entry_phone.grid(row=2, column=1)

        tk.Button(add_client_window, text="Сохранить", command=save_client).grid(row=3, column=0, columnspan=2)

    def add_car_to_client():
        """Добавить автомобиль выбранному клиенту."""
        selected_client = client_list.focus()
        if not selected_client:
            messagebox.showerror("Ошибка", "Выберите клиента.")
            return

        client_id = client_list.item(selected_client)['values'][0]

        def save_car():
            make = entry_make.get()
            year = entry_year.get()
            vin = entry_vin.get()
            if not make or not year or not vin:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            if not year.isdigit() or int(year) < 1900 or int(year) > 2100:
                messagebox.showerror("Ошибка", "Введите корректный год выпуска!")
                return
            add_car(client_id, make, int(year), vin)
            messagebox.showinfo("Успех", "Автомобиль добавлен.")
            add_car_window.destroy()

        # Окно добавления автомобиля
        add_car_window = tk.Toplevel(window)
        add_car_window.title("Добавить автомобиль")

        tk.Label(add_car_window, text="Марка автомобиля:").grid(row=0, column=0, padx=10, pady=5)
        entry_make = tk.Entry(add_car_window)
        entry_make.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_car_window, text="Год выпуска:").grid(row=1, column=0, padx=10, pady=5)
        entry_year = tk.Entry(add_car_window)
        entry_year.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_car_window, text="VIN:").grid(row=2, column=0, padx=10, pady=5)
        entry_vin = tk.Entry(add_car_window)
        entry_vin.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(add_car_window, text="Сохранить", command=save_car).grid(row=3, column=0, columnspan=2, pady=10)

    def delete_client():
        """Удалить выбранного клиента из базы данных."""
        selected_client = client_list.focus()
        if not selected_client:
            messagebox.showerror("Ошибка", "Выберите клиента.")
            return

        client_id = client_list.item(selected_client)['values'][0]

        import sqlite3
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clients WHERE ClientID = ?", (client_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Клиент удален.")
        refresh_client_list()

    # Главное окно управления клиентами
    window = tk.Tk()
    window.title("Управление клиентами")
    window.geometry("600x400")

    # Список клиентов
    client_list = ttk.Treeview(window, columns=("ID", "Имя", "Фамилия", "Телефон"), show="headings", height=15)
    client_list.heading("ID", text="ID")
    client_list.heading("Имя", text="Имя")
    client_list.heading("Фамилия", text="Фамилия")
    client_list.heading("Телефон", text="Телефон")
    client_list.column("ID", width=50)
    client_list.column("Имя", width=150)
    client_list.column("Фамилия", width=150)
    client_list.column("Телефон", width=200)
    client_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Кнопки управления
    tk.Button(window, text="Добавить клиента", command=open_add_client_window).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(window, text="Добавить автомобиль", command=add_car_to_client).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(window, text="Удалить клиента", command=delete_client).pack(side=tk.LEFT, padx=10, pady=10)

    # Загрузить список клиентов
    refresh_client_list()

    window.mainloop()
