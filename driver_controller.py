from flask import Blueprint, jsonify, request
from app.services.driver_service import DriverService

driver_bp = Blueprint('drivers', __name__)
driver_service = DriverService()


@driver_bp.route('/api/drivers/all', methods=['GET'])
def get_all_drivers():
    """
    Обробляє GET-запит на /api/drivers/all.
    Повертає всі записи з таблиці Drivers.
    """
    try:
        result_data = driver_service.get_all_drivers()

        return jsonify({
            "status": "success",
            "count": len(result_data),
            "data": result_data
        }), 200

    except Exception as e:
        print(f"Помилка при отриманні всіх водіїв: {e}")
        return jsonify({"status": "error", "message": f"Помилка сервера: {e}"}), 500


@driver_bp.route('/api/drivers', methods=['POST'])
def create_driver():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Недійсний формат JSON або порожні дані"}), 400

    # !!! ОНОВЛЕНІ ОБОВ'ЯЗКОВІ ПОЛЯ: очікуємо first_name та last_name окремо !!!
    required_fields = ['quarry_id', 'first_name', 'last_name', 'license_number']
    if not all(field in data for field in required_fields):
        return jsonify({
            "status": "error",
            "message": f"Відсутні обов'язкові поля: {', '.join(required_fields)}. Зверніть увагу: Ім'я та Прізвище мають бути окремими полями."
        }), 400

    # !!! Блок обробки 'full_name' ВИДАЛЕНО, оскільки ми очікуємо окремі поля !!!
    processed_data = {
        'quarry_id': data['quarry_id'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'license_number': data['license_number']
        # Можна додати інші поля, якщо вони є у JSON, наприклад:
        # 'date_of_birth': data.get('date_of_birth'),
        # 'experience_years': data.get('experience_years')
    }

    try:
        # Виклик сервісу передає дані "як є"
        new_id = driver_service.create_driver(processed_data)

        return jsonify({
            "status": "success",
            "id": new_id,
            "message": "Водій успішно доданий"
        }), 201

    except Exception as e:
        # Обробка помилок бази даних (наприклад, порушення унікальності license_number або тригера формату)
        error_msg = str(e).replace('\n', ' ')
        print(f"Помилка бази даних при створенні водія: {error_msg}")

        # Повернення 400, якщо це помилка, пов'язана з вхідними даними (наприклад, порушення тригера)
        if "SQLSTATE '45000'" in error_msg:
            return jsonify({"status": "error", "message": f"Помилка валідації даних: {error_msg}"}), 400

        return jsonify({"status": "error", "message": f"Помилка сервера: {error_msg}"}), 500


# Припустимо, що 'driver_bp' та 'driver_service' вже ініціалізовані та імпортовані

@driver_bp.route('/api/drivers/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Недійсний формат JSON або порожні дані"}), 400

    # Словник для передачі в сервіс
    processed_data = data.copy()

    # === КОРЕКЦІЯ: Обробка full_name, якщо воно надіслане ===
    if 'full_name' in processed_data:
        full_name_parts = processed_data.pop('full_name').strip().split(' ', 1)

        if len(full_name_parts) >= 1:
            # Обов'язково додаємо first_name
            processed_data['first_name'] = full_name_parts[0]

            # Додаємо last_name, якщо воно існує
            if len(full_name_parts) > 1:
                processed_data['last_name'] = full_name_parts[1]
            else:
                # Це оновлення, тому ми не повинні примусово встановлювати порожнє прізвище,
                # якщо клієнт надіслав лише ім'я, тому пропустимо це.
                pass

                # === Кінець обробки full_name ===

    try:
        rows_affected = driver_service.update_driver(driver_id, processed_data)

        if rows_affected > 0:
            return jsonify({"status": "success", "message": "Водій успішно оновлений"}), 200

        # Якщо 0 рядків оновлено, це може бути через те, що ID не знайдено, або дані не змінилися
        return jsonify({"status": "error", "message": "Водія з таким ID не знайдено або дані не змінилися"}), 404

    except Exception as e:
        error_msg = str(e).replace('\n', ' ')
        print(f"Помилка бази даних при оновленні водія: {error_msg}")

        # Обробка помилок бази даних (тригери, унікальність)
        if "SQLSTATE '45000'" in error_msg or "Duplicate entry" in error_msg:
            return jsonify({"status": "error", "message": f"Помилка валідації/унікальності: {error_msg}"}), 400

        return jsonify({"status": "error", "message": f"Помилка сервера: {error_msg}"}), 500


@driver_bp.route('/api/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    # Логіка DELETE залишається простою, оскільки вона не обробляє вхідні дані
    try:
        rows_affected = driver_service.delete_driver(driver_id)

        if rows_affected > 0:
            return jsonify({"status": "success", "message": "Водій успішно видалений"}), 200

        return jsonify({"status": "error", "message": "Водія з таким ID не знайдено"}), 404

    except Exception as e:
        error_msg = str(e).replace('\n', ' ')
        print(f"Помилка бази даних при видаленні водія: {error_msg}")

        # Обробка помилок FK (якщо є пов'язані записи)
        if "Cannot delete or update parent row: a foreign key constraint fails" in error_msg:
            return jsonify({"status": "error",
                            "message": "Неможливо видалити водія: існують пов'язані записи (Foreign Key Constraint)."}), 400

        return jsonify({"status": "error", "message": f"Помилка сервера: {error_msg}"}), 500