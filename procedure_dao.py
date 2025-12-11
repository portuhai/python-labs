# Файл: app/dao/procedure_dao.py (ОНОВЛЕНО)
from app import mysql
try:
    from MySQLdb.cursors import DictCursor
except ImportError:
    # Якщо використовується PyMySQL, імпорт інший, але часто Flask-MySQLdb
    # надає доступ через об'єкт connection
    DictCursor = None
    print("Warning: DictCursor from MySQLdb not found. Using basic cursor.")

class ProcedureDAO:
    def execute_procedure_no_return(self, proc_name, args=()):
        """Виконує процедуру без повернення SELECT-результату, використовуючи цикл nextset()."""

        # Використовуйте стандартний курсор
        cur = mysql.connection.cursor()

        try:
            cur.callproc(proc_name, args)

            # 1. ВИПРАВЛЕННЯ: Використовуємо nextset для очищення буфера результатів
            # Це необхідно, коли процедура не повертає набір результатів (SELECT)
            while cur.nextset():
                pass

            mysql.connection.commit()
            return {"status": "success", "message": f"Procedure {proc_name} executed."}
        except Exception as e:
            mysql.connection.rollback()
            raise Exception(f"Database error executing {proc_name}: {e}")
        finally:
            cur.close()

    def execute_procedure_with_output(self, proc_name, args=()):
        """Виконує процедуру, яка повертає SELECT, використовуючи DictCursor або базовий курсор."""

        # 2. Використовуємо DictCursor, якщо він імпортований, інакше - базовий курсор
        if DictCursor:
            cur = mysql.connection.cursor(DictCursor)
        else:
            # Це буде базовий курсор (повертає кортежі)
            cur = mysql.connection.cursor()

        try:
            cur.callproc(proc_name, args)
            data = cur.fetchall()

            # Обов'язкове очищення буфера (для всіх типів курсорів)
            while cur.nextset():
                pass

            mysql.connection.commit()

            # 3. Якщо DictCursor не спрацював, ми повернемо кортежі.
            # Обробка кортежів має бути у контролері (results[0][0])
            return data

        except Exception as e:
            mysql.connection.rollback()
            raise Exception(f"Database error executing {proc_name}: {e}")
        finally:
            cur.close()