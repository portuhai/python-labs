from app.dao.driver_dao import DriverDAO
from app.dtos.driver_dto import DriverDTO


class DriverService:
    """
    Сервіс для роботи з водіями. Містить бізнес-логіку.
    """

    def __init__(self):
        self.driver_dao = DriverDAO()

    def get_all_drivers(self):
        """ Отримати всі записи водіїв без фільтрації. """
        raw_drivers = self.driver_dao.get_all_drivers()

        return raw_drivers

    def create_driver(self, data):
        return self.driver_dao.create_driver(data)

    def update_driver(self, driver_id, data):
        return self.driver_dao.update_driver(driver_id, data)

    def delete_driver(self, driver_id):
        return self.driver_dao.delete_driver(driver_id)