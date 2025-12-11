from flask import Blueprint, jsonify
from app.services.shift_service import ShiftService

shift_bp = Blueprint('shifts', __name__)
shift_service = ShiftService()


@shift_bp.route('/api/shifts/all-assignments', methods=['GET']) # Змінено шлях
def get_all_assignments_details(): # Змінено назву функції
    """
    Обробляє GET-запит на /api/shifts/all-assignments
    Повертає деталі всіх призначень (водій, транспорт, зміна) за весь час.
    """
    try:
        # Змінено виклик методу
        result_dtos = shift_service.get_all_assignments_details()

        return jsonify({
            "status": "success",
            "count": len(result_dtos),
            "data": result_dtos
        }), 200

    except Exception as e:
        print(f"Помилка при отриманні деталей призначень: {e}")
        return jsonify({"status": "error", "message": f"Помилка сервера: {e}"}), 500