import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def work_history_window():
    def fetch_work_history():
        """Получение истории работ с информацией об автомобиле и владельце."""
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                WorkHistory.WorkID,
                WorkHistory.Date, 
                WorkHistory.Description, 
                WorkHistory.TotalCost, 
                Cars.Make || ' (' || Cars.Year || ')' AS CarInfo, 
                Clients.FirstName || ' ' || Clients.LastName AS OwnerInfo
            FROM WorkHistory
            JOIN Cars ON WorkHistory.OrderID = Cars.CarID
            JOIN Clients ON Cars.ClientID = Clients.ClientID
            ORDER BY WorkHistory.Date DESC
        ''')
        work_history = cursor.fetchall()
        conn.close()
        return work_history

    def refresh_work_list():
        """Обновить список работ."""
        work_list.delete(*work_list.get_children())
        for work in fetch_work_history():
            work_list.insert("", "end", values=(work[0], work[1], work[2], work[3], work[4], work[5]))

    def delete_work():
        """Удалить выбранную запись из истории."""
        selected_work = work_list.focus()
        if not selected_work:
            messagebox.showerror("Ошибка", "Выберите запись для удаления.")
            return

        work_id = work_list.item(selected_work)['values'][0]

        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM WorkHistory WHERE WorkID = ?", (work_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Запись удалена.")
        refresh_work_list()

    def open_add_work_window():
        """Открыть окно добавления новой записи."""

        def save_work():
            date = entry_date.get()
            description = entry_description.get()
            total_cost = entry_total_cost.get()
            car_id = entry_car_id.get()

            if not date or not description or not total_cost or not car_id:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            try:
                total_cost = float(total_cost)
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную сумму!")
                return

            conn = sqlite3.connect('autoshop.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO WorkHistory (OrderID, Date, Description, TotalCost)
                VALUES (?, ?, ?, ?)
            ''', (car_id, date, description, total_cost))
            conn.commit()
            conn.close()

            messagebox.showinfo("Успех", "Запись добавлена.")
            add_work_window.destroy()
            refresh_work_list()

        # Окно добавления записи
        add_work_window = tk.Toplevel(window)
        add_work_window.title("Добавить запись")

        tk.Label(add_work_window, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=10, pady=5)
        entry_date = tk.Entry(add_work_window)
        entry_date.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_work_window, text="Описание:").grid(row=1, column=0, padx=10, pady=5)
        entry_description = tk.Entry(add_work_window)
        entry_description.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_work_window, text="Стоимость:").grid(row=2, column=0, padx=10, pady=5)
        entry_total_cost = tk.Entry(add_work_window)
        entry_total_cost.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_work_window, text="ID автомобиля:").grid(row=3, column=0, padx=10, pady=5)
        entry_car_id = tk.Entry(add_work_window)
        entry_car_id.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(add_work_window, text="Сохранить", command=save_work).grid(row=4, column=0, columnspan=2, pady=10)

    def open_edit_work_window():
        """Открыть окно редактирования выбранной записи."""
        selected_work = work_list.focus()
        if not selected_work:
            messagebox.showerror("Ошибка", "Выберите запись для редактирования.")
            return

        # Получить данные выбранной записи
        work_data = work_list.item(selected_work)['values']
        work_id = work_data[0]
        work_date = work_data[1]
        work_description = work_data[2]
        work_total_cost = work_data[3]

        def save_edited_work():
            new_date = entry_date.get()
            new_description = entry_description.get()
            new_total_cost = entry_total_cost.get()

            if not new_date or not new_description or not new_total_cost:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            try:
                new_total_cost = float(new_total_cost)
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную сумму!")
                return

            conn = sqlite3.connect('autoshop.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE WorkHistory
                SET Date = ?, Description = ?, TotalCost = ?
                WHERE WorkID = ?
            ''', (new_date, new_description, new_total_cost, work_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Успех", "Запись обновлена.")
            edit_work_window.destroy()
            refresh_work_list()

        # Окно редактирования записи
        edit_work_window = tk.Toplevel(window)
        edit_work_window.title("Редактировать запись")

        tk.Label(edit_work_window, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=10, pady=5)
        entry_date = tk.Entry(edit_work_window)
        entry_date.insert(0, work_date)
        entry_date.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_work_window, text="Описание:").grid(row=1, column=0, padx=10, pady=5)
        entry_description = tk.Entry(edit_work_window)
        entry_description.insert(0, work_description)
        entry_description.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_work_window, text="Стоимость:").grid(row=2, column=0, padx=10, pady=5)
        entry_total_cost = tk.Entry(edit_work_window)
        entry_total_cost.insert(0, work_total_cost)
        entry_total_cost.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(edit_work_window, text="Сохранить", command=save_edited_work).grid(row=3, column=0, columnspan=2,
                                                                                     pady=10)

    # Главное окно
    window = tk.Tk()
    window.title("История работ")
    window.geometry("800x400")

    # Список работ
    work_list = ttk.Treeview(
        window,
        columns=("WorkID", "Дата", "Описание", "Стоимость", "Информация об автомобиле", "Информация о владельце"),
        show="headings",
        height=15
    )
    work_list.heading("Дата", text="Дата")
    work_list.heading("Описание", text="Описание")
    work_list.heading("Стоимость", text="Стоимость")
    work_list.heading("Информация об автомобиле", text="Автомобиль")
    work_list.heading("Информация о владельце", text="Владелец")

    work_list.column("WorkID", width=0, stretch=False)
    work_list.column("Дата", width=100)
    work_list.column("Описание", width=250)
    work_list.column("Стоимость", width=100)
    work_list.column("Информация об автомобиле", width=200)
    work_list.column("Информация о владельце", width=150)

    work_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Кнопки управления
    tk.Button(window, text="Добавить запись", command=open_add_work_window).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(window, text="Удалить запись", command=delete_work).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(window, text="Редактировать запись", command=open_edit_work_window).pack(side=tk.LEFT, padx=10, pady=10)

    # Загрузить данные
    refresh_work_list()

    window.mainloop()
