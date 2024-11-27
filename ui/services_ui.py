import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database import add_service

def manage_services_window():
    def fetch_services():
        """Получение всех услуг из базы данных."""
        import sqlite3
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ServiceID, ServiceName, ServicePrice FROM Services")
        services = cursor.fetchall()
        conn.close()
        return services

    def refresh_service_list():
        """Обновить список услуг."""
        service_list.delete(*service_list.get_children())  # Очистить текущий список
        for service in fetch_services():
            service_list.insert("", "end", values=(service[0], service[1], service[2]))

    def open_add_service_window():
        """Открыть окно добавления новой услуги."""
        def save_service():
            service_name = entry_service_name.get()
            service_price = entry_service_price.get()
            if service_name and service_price:
                try:
                    add_service(service_name, float(service_price))
                    messagebox.showinfo("Успех", "Услуга добавлена.")
                    add_service_window.destroy()
                    refresh_service_list()
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректную цену.")
            else:
                messagebox.showerror("Ошибка", "Заполните все поля!")

        # Окно добавления услуги
        add_service_window = tk.Toplevel(window)
        add_service_window.title("Добавить услугу")

        tk.Label(add_service_window, text="Название услуги:").grid(row=0, column=0, padx=10, pady=5)
        entry_service_name = tk.Entry(add_service_window)
        entry_service_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_service_window, text="Цена:").grid(row=1, column=0, padx=10, pady=5)
        entry_service_price = tk.Entry(add_service_window)
        entry_service_price.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(add_service_window, text="Сохранить", command=save_service).grid(row=2, column=0, columnspan=2, pady=10)

    def delete_service():
        """Удалить выбранную услугу."""
        selected_service = service_list.focus()
        if not selected_service:
            messagebox.showerror("Ошибка", "Выберите услугу.")
            return

        service_id = service_list.item(selected_service)['values'][0]

        import sqlite3
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Services WHERE ServiceID = ?", (service_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Услуга удалена.")
        refresh_service_list()

    def edit_service():
        """Редактировать данные выбранной услуги."""
        selected_service = service_list.focus()
        if not selected_service:
            messagebox.showerror("Ошибка", "Выберите услугу.")
            return

        service_id, service_name, service_price = service_list.item(selected_service)['values']

        def save_edited_service():
            new_service_name = entry_service_name.get()
            new_service_price = entry_service_price.get()

            if new_service_name and new_service_price:
                try:
                    conn = sqlite3.connect('autoshop.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE Services
                        SET ServiceName = ?, ServicePrice = ?
                        WHERE ServiceID = ?
                    ''', (new_service_name, float(new_service_price), service_id))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Успех", "Данные услуги обновлены.")
                    edit_service_window.destroy()
                    refresh_service_list()
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректную цену.")
            else:
                messagebox.showerror("Ошибка", "Заполните все поля!")

        # Окно редактирования услуги
        edit_service_window = tk.Toplevel(window)
        edit_service_window.title("Редактировать услугу")

        tk.Label(edit_service_window, text="Название услуги:").grid(row=0, column=0, padx=10, pady=5)
        entry_service_name = tk.Entry(edit_service_window)
        entry_service_name.insert(0, service_name)
        entry_service_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_service_window, text="Цена:").grid(row=1, column=0, padx=10, pady=5)
        entry_service_price = tk.Entry(edit_service_window)
        entry_service_price.insert(0, service_price)
        entry_service_price.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(edit_service_window, text="Сохранить", command=save_edited_service).grid(row=2, column=0, columnspan=2, pady=10)

    # Главное окно
    window = tk.Tk()
    window.title("Управление услугами")
    window.geometry("600x400")

    # Список услуг
    service_list = ttk.Treeview(window, columns=("ID", "Название", "Цена"), show="headings", height=15)
    service_list.heading("ID", text="ID")
    service_list.heading("Название", text="Название")
    service_list.heading("Цена", text="Цена")
    service_list.column("ID", width=50)
    service_list.column("Название", width=300)
    service_list.column("Цена", width=100)
    service_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Кнопки управления
    tk.Button(window, text="Добавить услугу", command=open_add_service_window).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(window, text="Удалить услугу", command=delete_service).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(window, text="Редактировать услугу", command=edit_service).pack(side=tk.LEFT, padx=10, pady=10)

    # Загрузить список услуг
    refresh_service_list()

    window.mainloop()
