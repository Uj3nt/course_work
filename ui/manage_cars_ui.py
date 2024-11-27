import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def manage_cars_window():
    def fetch_cars():
        """Получение всех автомобилей из базы данных."""
        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                Cars.CarID, 
                Cars.Make, 
                Cars.Year, 
                Cars.VIN, 
                Clients.FirstName || ' ' || Clients.LastName AS OwnerInfo
            FROM Cars
            JOIN Clients ON Cars.ClientID = Clients.ClientID
        ''')
        cars = cursor.fetchall()
        conn.close()
        return cars

    def refresh_car_list():
        """Обновить список автомобилей."""
        car_list.delete(*car_list.get_children())
        for car in fetch_cars():
            car_list.insert("", "end", values=(car[0], car[1], car[2], car[3], car[4]))

    def delete_car():
        """Удалить выбранный автомобиль."""
        selected_car = car_list.focus()
        if not selected_car:
            messagebox.showerror("Ошибка", "Выберите автомобиль для удаления.")
            return

        car_id = car_list.item(selected_car)['values'][0]

        conn = sqlite3.connect('autoshop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cars WHERE CarID = ?", (car_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Автомобиль удален.")
        refresh_car_list()

    def open_edit_car_window():
        """Открыть окно редактирования выбранного автомобиля."""
        selected_car = car_list.focus()
        if not selected_car:
            messagebox.showerror("Ошибка", "Выберите автомобиль для редактирования.")
            return

        # Получить данные выбранного автомобиля
        car_data = car_list.item(selected_car)['values']
        car_id = car_data[0]
        car_make = car_data[1]
        car_year = car_data[2]
        car_vin = car_data[3]

        def save_edited_car():
            new_make = entry_make.get()
            new_year = entry_year.get()
            new_vin = entry_vin.get()

            if not new_make or not new_year or not new_vin:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            try:
                new_year = int(new_year)
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректный год!")
                return

            conn = sqlite3.connect('autoshop.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Cars
                SET Make = ?, Year = ?, VIN = ?
                WHERE CarID = ?
            ''', (new_make, new_year, new_vin, car_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Успех", "Данные автомобиля обновлены.")
            edit_car_window.destroy()
            refresh_car_list()

        # Окно редактирования автомобиля
        edit_car_window = tk.Toplevel(window)
        edit_car_window.title("Редактировать автомобиль")

        tk.Label(edit_car_window, text="Марка:").grid(row=0, column=0, padx=10, pady=5)
        entry_make = tk.Entry(edit_car_window)
        entry_make.insert(0, car_make)
        entry_make.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_car_window, text="Год выпуска:").grid(row=1, column=0, padx=10, pady=5)
        entry_year = tk.Entry(edit_car_window)
        entry_year.insert(0, car_year)
        entry_year.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_car_window, text="VIN:").grid(row=2, column=0, padx=10, pady=5)
        entry_vin = tk.Entry(edit_car_window)
        entry_vin.insert(0, car_vin)
        entry_vin.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(edit_car_window, text="Сохранить", command=save_edited_car).grid(row=3, column=0, columnspan=2,
                                                                                   pady=10)

    # Главное окно
    window = tk.Tk()
    window.title("Управление автомобилями")
    window.geometry("800x400")

    # Список автомобилей
    car_list = ttk.Treeview(
        window,
        columns=("ID", "Марка", "Год", "VIN", "Владелец"),
        show="headings",
        height=15
    )
    car_list.heading("ID", text="ID")
    car_list.heading("Марка", text="Марка")
    car_list.heading("Год", text="Год")
    car_list.heading("VIN", text="VIN")
    car_list.heading("Владелец", text="Владелец")

    car_list.column("ID", width=50)
    car_list.column("Марка", width=150)
    car_list.column("Год", width=100)
    car_list.column("VIN", width=200)
    car_list.column("Владелец", width=150)

    car_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Кнопки управления
    tk.Button(window, text="Удалить автомобиль", command=delete_car).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(window, text="Редактировать автомобиль", command=open_edit_car_window).pack(side=tk.LEFT, padx=10,
                                                                                          pady=10)

    # Загрузить список автомобилей
    refresh_car_list()

    window.mainloop()
