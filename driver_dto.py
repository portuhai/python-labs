class DriverDTO:
    """
    Об'єкт передачі даних для водія.
    Використовується для формування чистої відповіді клієнту.
    """

    def __init__(self, driver_id, first_name, last_name, quarry_name=None, check_result=None):
        # Ці поля відповідають структурі вашої БД
        self.driver_id = driver_id
        self.first_name = first_name
        self.last_name = last_name
        self.quarry_name = quarry_name
        self.check_result = check_result

    @property
    def full_name(self):
        """ Об'єднує ім'я та прізвище для зручності клієнта. """
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        """ Перетворення об'єкта DTO у словник для JSON-відповіді. """
        data = {
            'driver_id': self.driver_id,
            # Клієнт бачить full_name
            'full_name': self.full_name
        }
        # ... (решта полів) ...
        return data