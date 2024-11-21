from database import initialize_database
import tkinter as tk
from ui.clients_ui import manage_clients_window
from ui.orders_ui import create_order_window
from ui.services_ui import add_service_window
from ui.work_history_ui import work_history_window

def main():
    initialize_database()

    def open_clients():
        manage_clients_window()

    def open_orders():
        create_order_window()

    def open_services():
        add_service_window()

    def open_work_history():
        work_history_window()

    # Главное окно
    root = tk.Tk()
    root.title("Автомастерская")
    root.geometry("300x200")

    tk.Button(root, text="Управление клиентами", command=open_clients, width=30).pack(pady=10)
    tk.Button(root, text="Управление услугами", command=open_services, width=30).pack(pady=10)
    tk.Button(root, text="Добавление работ", command=open_orders, width=30).pack(pady=10)
    tk.Button(root, text="История работ", command=open_work_history, width=30).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
