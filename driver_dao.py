from app import mysql


class DriverDAO:
    """
    DAO (Data Access Object) для таблиці Drivers.
    Відповідає виключно за виконання SQL-запитів.
    """

    def get_all_drivers(self):
        """ Виводить усі записи з таблиці Drivers. """

        query = "SELECT * FROM Drivers;"

        cur = mysql.connection.cursor()
        cur.execute(query)

        data = cur.fetchall()
        cur.close()

        return data

    def create_driver(self, data):
        """
        Вставка даних у таблицю Drivers.
        ПРИМІТКА: Очікуємо data['first_name'] та data['last_name'].
        """
        query = """
        INSERT INTO Drivers (quarry_id, first_name, last_name, license_number) 
        VALUES (%s, %s, %s, %s)
        """
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (
                data['quarry_id'],
                data['first_name'],
                data['last_name'],
                data['license_number']
            ))
            mysql.connection.commit()
            driver_id = cur.lastrowid
            return driver_id
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cur.close()

    def update_driver(self, driver_id, data):
        """
        Оновлення даних у таблиці Drivers.
        Очікуємо data['first_name'] та data['last_name'] (якщо вони є в data).
        """

        # 1. Формуємо динамічний SET-вираз
        set_clauses = []
        params = []

        # Перевіряємо та додаємо first_name, last_name, якщо вони є (після розділення у контролері)
        if 'first_name' in data and 'last_name' in data:
            set_clauses.append("first_name = %s, last_name = %s")
            params.extend([data['first_name'], data['last_name']])
        elif 'first_name' in data:
            set_clauses.append("first_name = %s")
            params.append(data['first_name'])
        elif 'last_name' in data:
            set_clauses.append("last_name = %s")
            params.append(data['last_name'])

        # Додаємо quarry_id, якщо він є
        if 'quarry_id' in data:
            set_clauses.append("quarry_id = %s")
            params.append(data['quarry_id'])

        # Додаємо license_number, якщо він є
        if 'license_number' in data:
            set_clauses.append("license_number = %s")
            params.append(data['license_number'])

        if not set_clauses:
            # Нічого оновлювати
            return 0

        # 2. Складаємо фінальний запит
        query = f"UPDATE Drivers SET {', '.join(set_clauses)} WHERE driver_id = %s"
        params.append(driver_id)  # Додаємо ID в кінець

        cur = mysql.connection.cursor()
        try:
            cur.execute(query, tuple(params))
            mysql.connection.commit()
            return cur.rowcount
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cur.close()

    def delete_driver(self, driver_id):
        """ Видалення даних з таблиці Drivers. """
        query = "DELETE FROM Drivers WHERE driver_id = %s"
        cur = mysql.connection.cursor()
        try:
            cur.execute(query, (driver_id,))
            mysql.connection.commit()
            return cur.rowcount
        except Exception as e:
            # Якщо видалення неможливе через FK, викидаємо помилку
            mysql.connection.rollback()
            raise e
        finally:
            cur.close()
