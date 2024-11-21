import tkinter as tk
from tkinter import messagebox
from database import add_service

def add_service_window():
    def save_service():
        service_name = entry_service_name.get()
        service_price = entry_service_price.get()
        if service_name and service_price:
            try:
                add_service(service_name, float(service_price))
                messagebox.showinfo("Успех", "Услуга добавлена.")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную цену.")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля!")

    window = tk.Tk()
    window.title("Добавить услугу")

    tk.Label(window, text="Название услуги").grid(row=0, column=0)
    entry_service_name = tk.Entry(window)
    entry_service_name.grid(row=0, column=1)

    tk.Label(window, text="Цена").grid(row=1, column=0)
    entry_service_price = tk.Entry(window)
    entry_service_price.grid(row=1, column=1)

    tk.Button(window, text="Сохранить", command=save_service).grid(row=2, column=0, columnspan=2)
    window.mainloop()
