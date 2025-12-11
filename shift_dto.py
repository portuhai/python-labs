class ShiftDTO:
    """
    Об'єкт передачі даних для Призначення на Зміну (Driver Assignment).
    Об'єднує дані з `shifts`, `drivers` та `transports`.
    """

    def __init__(self, assignment_id, shift_id, shift_date, shift_number,
                 driver_first_name, driver_last_name, transport_serial_number, quarry_id, quarry_name=None):
        self.assignment_id = assignment_id
        self.shift_id = shift_id
        self.shift_number = shift_number
        self.quarry_id = quarry_id
        self.driver_name = f"{driver_first_name} {driver_last_name}"
        self.transport_serial_number = transport_serial_number
        self.quarry_name = quarry_name

        # ************************************************************
        # ВИПРАВЛЕННЯ: Безпечне форматування дати
        # Перевіряємо, чи є shift_date об'єктом, що підтримує strftime
        if hasattr(shift_date, 'strftime'):
            self.shift_date = shift_date.strftime('%Y-%m-%d')
        else:
            # Якщо це вже рядок або інший тип, просто використовуємо його
            self.shift_date = str(shift_date)
            # ************************************************************

    def to_dict(self):
        """ Перетворення об'єкта DTO у словник для JSON-відповіді. """
        data = {
            'assignment_id': self.assignment_id,
            'shift_id': self.shift_id,
            'shift_date': self.shift_date,
            'shift_number': self.shift_number,
            'driver_name': self.driver_name,
            'quarry_id': self.quarry_id,
            'transport_serial_number': self.transport_serial_number,
        }
        if self.quarry_name:
            data['quarry_name'] = self.quarry_name
        return data