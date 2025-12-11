from flask import Blueprint, jsonify
from app.services.vehicle_service import VehicleService

vehicle_bp = Blueprint('transports', __name__)
vehicle_service = VehicleService() # !!! ВИПРАВЛЕНО: Створюємо екземпляр правильного класу !!!


# Завдання M:1
@vehicle_bp.route('/api/quarries/<int:quarry_id>/transports', methods=['GET'])
def get_vehicles_by_quarry(quarry_id):
    """
    Обробляє GET-запит на /api/quarries/<id>/transports
    Повертає всю техніку, приписану до вказаного кар'єру.
    """
    try:
        # ВИПРАВЛЕНО: Викликаємо метод на правильному об'єкті 'transport_service'
        result_dtos = vehicle_service.get_vehicles_by_quarry(quarry_id)

        return jsonify({
            "status": "success",
            "count": len(result_dtos),
            "data": result_dtos
        }), 200

    except Exception as e:
        print(f"Помилка при отриманні техніки: {e}")
        return jsonify({"status": "error", "message": f"Помилка сервера: {e}"}), 500