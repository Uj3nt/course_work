import sqlite3

# Создание базы данных и таблиц
def initialize_database():
    conn = sqlite3.connect('autoshop.db')
    cursor = conn.cursor()

    # Таблица клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        PhoneNumber TEXT NOT NULL
    )
    ''')

    # Таблица автомобилей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cars (
        CarID INTEGER PRIMARY KEY AUTOINCREMENT,
        ClientID INTEGER NOT NULL,
        Make TEXT NOT NULL,
        Model TEXT NOT NULL,
        Year INTEGER NOT NULL,
        VIN TEXT NOT NULL,
        FOREIGN KEY (ClientID) REFERENCES Clients (ClientID)
    )
    ''')

    # Таблица заказов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        CarID INTEGER NOT NULL,
        OrderDate DATE NOT NULL,
        TotalCost REAL DEFAULT 0.0,
        FOREIGN KEY (CarID) REFERENCES Cars (CarID)
    )
    ''')

    # Таблица услуг
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Services (
        ServiceID INTEGER PRIMARY KEY AUTOINCREMENT,
        ServiceName TEXT NOT NULL,
        ServicePrice REAL NOT NULL
    )
    ''')

    # Таблица связи заказов и услуг
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS OrderServices (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderID INTEGER NOT NULL,
        ServiceID INTEGER NOT NULL,
        FOREIGN KEY (OrderID) REFERENCES Orders (OrderID),
        FOREIGN KEY (ServiceID) REFERENCES Services (ServiceID)
    )
    ''')

    conn.commit()
    conn.close()

# Функции для работы с данными
def add_client(first_name, last_name, phone_number):
    conn = sqlite3.connect('autoshop.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Clients (FirstName, LastName, PhoneNumber)
        VALUES (?, ?, ?)
    ''', (first_name, last_name, phone_number))
    conn.commit()
    conn.close()

def add_car(client_id, make, year, vin):
    conn = sqlite3.connect('autoshop.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Cars (ClientID, Make, Year, VIN)
        VALUES (?, ?, ?, ?)
    ''', (client_id, make, year, vin))
    conn.commit()
    conn.close()

def add_service(service_name, service_price):
    conn = sqlite3.connect('autoshop.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Services (ServiceName, ServicePrice)
        VALUES (?, ?)
    ''', (service_name, service_price))
    conn.commit()
    conn.close()

def create_order(car_id, service_ids):
    conn = sqlite3.connect('autoshop.db')
    cursor = conn.cursor()

    # Создание заказа
    cursor.execute('''
        INSERT INTO Orders (CarID, OrderDate)
        VALUES (?, date('now'))
    ''', (car_id,))
    order_id = cursor.lastrowid

    # Связывание заказа с услугами
    total_cost = 0
    for service_id in service_ids:
        cursor.execute('''
            INSERT INTO OrderServices (OrderID, ServiceID)
            VALUES (?, ?)
        ''', (order_id, service_id))
        cursor.execute('SELECT ServicePrice FROM Services WHERE ServiceID = ?', (service_id,))
        total_cost += cursor.fetchone()[0]

    # Обновление стоимости заказа
    cursor.execute('''
        UPDATE Orders
        SET TotalCost = ?
        WHERE OrderID = ?
    ''', (total_cost, order_id))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WorkHistory (
            WorkID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderID INTEGER NOT NULL,
            Date DATE NOT NULL,
            Description TEXT NOT NULL,
            TotalCost REAL NOT NULL,
            FOREIGN KEY (OrderID) REFERENCES Orders (OrderID)
        )
        ''')

    conn.commit()
    conn.close()
