import tkinter as tk

from database import initialize_database
from ui.clients_ui import manage_clients_window
from ui.add_work_ui import add_work_window
from ui.work_history_ui import work_history_window
from ui.services_ui import manage_services_window
from ui.manage_cars_ui import manage_cars_window


def main():
    initialize_database()

    def open_clients():
        manage_clients_window()

    def open_services():
        manage_services_window()

    def open_work_history():
        work_history_window()

    def open_add_work():
        add_work_window()

    # Главное меню
    root = tk.Tk()
    root.title("Автомастерская")
    root.geometry("380x300")

    tk.Button(root, text="Управление клиентами", command=open_clients, width=30).pack(pady=10)
    tk.Button(root, text="Управление услугами", command=open_services, width=30).pack(pady=10)
    tk.Button(root, text="Управление автомобилями", command=manage_cars_window, width=30).pack(pady=10)
    tk.Button(root, text="Добавить работу", command=open_add_work, width=30).pack(pady=10)
    tk.Button(root, text="История работ", command=open_work_history, width=30).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
