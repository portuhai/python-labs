# Файл: app/services/vehicle_service.py (ВИПРАВЛЕНО)

from app.dao.vehicle_dao import VehicleDAO
from app.dtos.vehicle_dto import VehicleDTO


class VehicleService:
    """
    Сервіс для роботи з технікою (Vehicles).
    """

    def __init__(self):
        self.vehicle_dao = VehicleDAO()

    def get_vehicles_by_quarry(self, quarry_id):
        """
        Отримати список техніки, приписаної до певного кар'єру, використовуючи числові індекси.
        """
        # 1. Отримати сирі дані (кортежі) з бази через DAO
        raw_vehicles = self.vehicle_dao.get_vehicles_by_quarry(quarry_id)

        # 2. Перетворити сирі дані (кортежі) у список DTO-об'єктів (словників)
        vehicle_dtos = []
        for vehicle_row in raw_vehicles:
            # ************************************************************
            # ВИПРАВЛЕННЯ: Доступ до елементів кортежу лише за ЧИСЛОВИМ ІНДЕКСОМ
            dto = VehicleDTO(
                transport_id=vehicle_row[0],  # t.transport_id (Індекс 0)
                type_name=vehicle_row[1],  # tt.type_name (Індекс 1)
                model=vehicle_row[2],  # t.model (Індекс 2)
                serial_number=vehicle_row[3],  # t.serial_number (Індекс 3)
                status=vehicle_row[4],  # t.status (Індекс 4)
                quarry_name=vehicle_row[5]  # q.name (Індекс 5)
            )
            # ************************************************************

            # Додаємо DTO у вигляді словника для JSON-відповіді
            vehicle_dtos.append(dto.to_dict())

        return vehicle_dtos