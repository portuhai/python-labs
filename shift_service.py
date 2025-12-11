# Файл: app/services/shift_service.py
from app.dao.shift_dao import ShiftDAO
from app.dtos.shift_dto import ShiftDTO  # Переконайтеся, що ви імпортуєте DTO


class ShiftService:
    def __init__(self):
        self.shift_dao = ShiftDAO()

    def get_all_assignments_details(self):
        """
        Отримує деталі призначень (кортежі) і перетворює їх на список DTO.
        """
        # 1. Отримуємо сирі дані (список кортежів)
        raw_assignments = self.shift_dao.get_all_assignments_details()

        assignment_dtos = []

        # 2. Обробка кортежів за числовими індексами
        for row in raw_assignments:
            # Створюємо DTO, використовуючи ЧИСЛОВІ ІНДЕКСИ відповідно до таблиці вище
            dto = ShiftDTO(
                assignment_id=row[0],
                shift_id=row[1],
                shift_date=row[2],  # Дата знаходиться на індексі 2
                shift_number=row[3],  # Номер зміни знаходиться на індексі 3
                quarry_id=row[4],  # ID кар'єру знаходиться на індексі 4
                driver_first_name=row[5],  # Ім'я водія знаходиться на індексі 5
                driver_last_name=row[6],  # Прізвище водія знаходиться на індексі 6
                transport_serial_number=row[7],  # Серійний номер транспорту знаходиться на індексі 7
                quarry_name=row[8]  # Назва кар'єру знаходиться на індексі 8
            )
            assignment_dtos.append(dto.to_dict())

        return assignment_dtos