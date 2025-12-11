class VehicleDTO:
    """
    Об'єкт передачі даних для техніки (Transport).
    Поля відповідають структурі таблиці `transports`.
    """
    def __init__(self, transport_id, type_name, model, serial_number, status, quarry_name=None):
        self.transport_id = transport_id
        # type_name - назва типу, отримана з таблиці transport_types (через JOIN)
        self.type_name = type_name # Атрибут тепер називається type_name
        self.model = model
        self.serial_number = serial_number
        self.status = status
        self.quarry_name = quarry_name

    def to_dict(self):
        """ Перетворення об'єкта DTO у словник для JSON-відповіді. """
        data = {
            'transport_id': self.transport_id,
            # ВИПРАВЛЕНО: Назва ключа у JSON має бути 'type', але дані беремо з type_name
            'type': self.type_name,
            'model': self.model,
            'serial_number': self.serial_number,
            'status': self.status
        }
        if self.quarry_name:
            data['quarry_name'] = self.quarry_name
        return data