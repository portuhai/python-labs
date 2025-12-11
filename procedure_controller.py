from flask import Blueprint, jsonify, request
from app.dao.procedure_dao import ProcedureDAO

procedure_bp = Blueprint('procedures', __name__)
proc_dao = ProcedureDAO()


# --- 1. Виклик: InsertNewMaintenanceLog (Параметризована вставка) ---
@procedure_bp.route('/api/procedures/maintenance/log', methods=['POST'])
def call_insert_maintenance_log():
    data = request.json
    required_fields = ['transport_id', 'maintenance_date', 'description', 'cost']
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields."}), 400

    try:
        proc_dao.execute_procedure_no_return(
            'InsertNewMaintenanceLog',
            (data['transport_id'], data['maintenance_date'], data['description'], data['cost'])
        )
        return jsonify({"status": "success", "message": "Maintenance log added via procedure."}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# --- 2. Виклик: AssignDriverByDetails (M:M зв'язок) ---
@procedure_bp.route('/api/procedures/driver/assign', methods=['POST'])
def call_assign_driver():
    data = request.json
    required_fields = ['shift_id', 'driver_first_name', 'driver_last_name', 'transport_serial_number']
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields for assignment."}), 400

    try:
        proc_dao.execute_procedure_no_return(
            'AssignDriverByDetails',
            (data['shift_id'], data['driver_first_name'], data['driver_last_name'], data['transport_serial_number'])
        )
        return jsonify({"status": "success", "message": "Driver assigned to transport via M:M procedure."}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# --- 3. Виклик: InsertTenDummyMaintenanceLogs (Пакетна вставка) ---
@procedure_bp.route('/api/procedures/maintenance/bulk-insert', methods=['POST'])
def call_bulk_insert():
    # Отримуємо початковий індекс з тіла або використовуємо 0
    p_start_index = request.json.get('start_index', 0) if request.json else 0
    try:
        proc_dao.execute_procedure_no_return(
            'InsertTenDummyMaintenanceLogs',
            (p_start_index,)
        )
        return jsonify(
            {"status": "success", "message": f"10 dummy logs inserted starting from index {p_start_index}."}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# --- 4. Виклик: GetQuarryCapacityAggregate (Процедура з функцією) ---
@procedure_bp.route('/api/procedures/quarry/aggregate', methods=['GET'])
def call_quarry_aggregate():
    operation = request.args.get('op', 'SUM').upper()
    if operation not in ['MAX', 'MIN', 'SUM', 'AVG']:
        return jsonify({"status": "error", "message": "Invalid operation. Use MAX, MIN, SUM, or AVG."}), 400

    try:
        # !!! ЗМІНА ТУТ: передаємо лише один аргумент (operation,)
        results = proc_dao.execute_procedure_with_output(
            'GetQuarryCapacityAggregate',
            (operation,)
        )

        # Обробка результату (якщо DAO повертає словники або кортежі)
        if results and results[0]:
            if isinstance(results[0], dict):
                # Якщо DAO повернув DictCursor (словник)
                aggregate_value = results[0].get('aggregate_value')
            else:
                # Якщо DAO повернув базовий курсор (кортеж)
                aggregate_value = results[0][0]

            return jsonify({
                "status": "success",
                "operation": operation,
                "value": aggregate_value
            }), 200
        else:
            return jsonify({"status": "error", "message": "No data returned or operation failed."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@procedure_bp.route('/api/procedures/transports/split', methods=['POST'])
def call_split_transports():
    try:
        # Процедура повертає SELECT: SELECT CONCAT(...) AS status_message
        results = proc_dao.execute_procedure_with_output('SplitTransportsRandomly')

        status_message = "Procedure executed successfully, but status message could not be retrieved."

        if results and results[0]:
            if isinstance(results[0], dict):
                # DictCursor
                status_message = results[0].get('status_message', status_message)
            else:
                # Базовий курсор (кортеж)
                status_message = results[0][0]

        return jsonify({"status": "success", "message": status_message}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500