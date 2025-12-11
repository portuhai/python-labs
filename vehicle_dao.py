from app import mysql
from app.dtos.vehicle_dto import VehicleDTO # Клас DTO називається VehicleDTO


class VehicleDAO: # Клас DAO, який фактично виконує запити до БД
    """
    DAO для таблиці transports (техніка).
    """

    def get_vehicles_by_quarry(self, quarry_id):
        """
        Виводить усю техніку (transports), приписану до певного кар'єру (quarries).
        """
        query = """
        SELECT 
            t.transport_id, 
            tt.type_name AS type_name, -- ПЕРЕЙМЕНОВАНО АЛІАС: type_name для DTO
            t.model, 
            t.serial_number, 
            t.status,
            q.name AS quarry_name
        FROM transports t
        JOIN quarries q ON t.quarry_id = q.quarry_id
        JOIN transport_types tt ON t.type_id = tt.type_id
        WHERE t.quarry_id = %s;
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (quarry_id,))
        data = cur.fetchall()
        cur.close()
        return data # Повертає список словників/кортежів