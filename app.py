from flask import Flask
from config import Config
from app import mysql
from app.controllers.driver_controller import driver_bp
from app.controllers.vehicle_controller import vehicle_bp
from app.controllers.shift_controller import shift_bp
from app.controllers.procedure_controller import procedure_bp

app = Flask(__name__)
app.config.from_object(Config)
mysql.init_app(app)
app.register_blueprint(driver_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(shift_bp)
app.register_blueprint(procedure_bp)


def get_db_connection():
    """Створює та повертає нове з'єднання з базою даних."""
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return "Quarry Transport API is running!"

if __name__ == '__main__':
    app.run(debug=True)