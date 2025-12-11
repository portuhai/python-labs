from app import mysql


class ShiftDAO:
    """
    DAO для таблиць shifts та driver_assignments.
    """

    def get_all_assignments_details(self):
        """
        Завдання M:M: Виводить усі призначення (driver_assignments) із зазначенням
        водія, транспорту та деталей зміни, включаючи назву кар'єру.
        """
        query = """
        SELECT 
            da.assignment_id,
            da.shift_id,
            s.shift_date,
            s.shift_number,
            s.quarry_id,
            d.first_name,
            d.last_name,
            t.serial_number AS transport_serial_number,
            q.name AS quarry_name                 -- <--- ДОДАНО
        FROM driver_assignments da
        JOIN shifts s ON da.shift_id = s.shift_id
        JOIN drivers d ON da.driver_id = d.driver_id
        JOIN transports t ON da.transport_id = t.transport_id
        JOIN quarries q ON s.quarry_id = q.quarry_id; -- <--- ДОДАНО JOIN
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data