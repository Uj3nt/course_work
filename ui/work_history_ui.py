import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def work_history_window():
    def fetch_work_history(sort_by_date=False):
        """Получение истории работ из базы данных."""
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        if sort_by_date:
            cursor.execute("SELECT * FROM WorkHistory ORDER BY Date")
        else:
            cursor.execute("SELECT * FROM WorkHistory")
        work_history = cursor.fetchall()
        conn.close()
        return work_history

    def refresh_work_list():
        """Обновить список работ."""
        work_list.delete(*work_list.get_children())  # Очистить текущий список
        for work in fetch_work_history(sort_by_date=sort_by_date.get()):
            work_list.insert("", "end", values=(work[0], work[1], work[2], work[3], work[4]))

    def open_add_work_window():
        """Открыть окно добавления новой работы."""
        def save_work():
            try:
                order_id = int(entry_order_id.get())
                date = entry_date.get()
                description = entry_description.get()
                total_cost = float(entry_total_cost.get())

                if not description or not date or not total_cost:
                    raise ValueError("Заполните все поля!")

                conn = sqlite3.connect('autoshop.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO WorkHistory (OrderID, Date, Description, TotalCost)
                    VALUES (?, ?, ?, ?)
                ''', (order_id, date, description, total_cost))
                conn.commit()
                conn.close()

                messagebox.showinfo("Успех", "Запись о работе добавлена.")
                add_work_window.destroy()
                refresh_work_list()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

        # Окно добавления работы
        add_work_window = tk.Toplevel(window)
        add_work_window.title("Добавить запись о работе")

        tk.Label(add_work_window, text="ID заказа:").grid(row=0, column=0, padx=10, pady=5)
        entry_order_id = tk.Entry(add_work_window)
        entry_order_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_work_window, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0, padx=10, pady=5)
        entry_date = tk.Entry(add_work_window)
        entry_date.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_work_window, text="Описание:").grid(row=2, column=0, padx=10, pady=5)
        entry_description = tk.Entry(add_work_window)
        entry_description.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_work_window, text="Стоимость:").grid(row=3, column=0, padx=10, pady=5)
        entry_total_cost = tk.Entry(add_work_window)
        entry_total_cost.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(add_work_window, text="Сохранить", command=save_work).grid(row=4, column=0, columnspan=2, pady=10)

    # Главное окно
    window = tk.Tk()
    window.title("История работ")
    window.geometry("700x400")

    # Переключатель сортировки
    sort_by_date = tk.BooleanVar(value=False)
    tk.Checkbutton(window, text="Сортировать по дате", variable=sort_by_date, command=refresh_work_list).pack(pady=5)

    # Список работ
    work_list = ttk.Treeview(window, columns=("ID", "OrderID", "Дата", "Описание", "Стоимость"), show="headings", height=15)
    work_list.heading("ID", text="ID")
    work_list.heading("OrderID", text="ID заказа")
    work_list.heading("Дата", text="Дата")
    work_list.heading("Описание", text="Описание")
    work_list.heading("Стоимость", text="Стоимость")
    work_list.column("ID", width=50)
    work_list.column("OrderID", width=100)
    work_list.column("Дата", width=100)
    work_list.column("Описание", width=250)
    work_list.column("Стоимость", width=100)
    work_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Кнопка добавления новой работы
    tk.Button(window, text="Добавить работу", command=open_add_work_window).pack(pady=10)

    # Загрузить историю работ
    refresh_work_list()

    window.mainloop()
