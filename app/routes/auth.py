from flask import Blueprint, request, jsonify
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.utils.database import get_db_connection
from flask import current_app

auth = Blueprint('auth', __name__)

@auth.route('/create_table', methods=['GET'])
def create_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()    

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            roles VARCHAR(255) NOT NULL
        );
        """

        cursor.execute(create_table_sql)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Table created successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        roles = data.get('roles', 'Data Entry Staff')
       
        if not email or not password:
            return jsonify({"error": "Email and password are required!"}), 400
       
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
       
        connection = get_db_connection()
        cursor = connection.cursor()
       
        insert_sql = """
        INSERT INTO users (email, user_name, password, roles)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_sql, (email, username, hashed_password.decode('utf-8'), roles))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "User added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth.route('/get_user', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required!"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, email, user_name, password, roles FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            cursor.execute("SELECT id, email, username, password, role, ownername FROM worker WHERE email = %s", (email,))
            worker = cursor.fetchone()

            if worker:
                user = worker
                is_worker = True
            else:
                user = None
                is_worker = False
        else:
            is_worker = False

        cursor.close()
        connection.close()

        if user:
            if is_worker:
                user_id, user_email, username, hashed_password, roles, ownername = user
            else:
                user_id, user_email, username, hashed_password, roles = user
                ownername = None

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                token_payload = {
                    "user_id": user_id,
                    "email": user_email,
                    "username": username,
                    "roles": roles,
                    "ownername": ownername if is_worker else None,
                    "exp": datetime.utcnow() + timedelta(hours=1)
                }
                token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm="HS256")

                return jsonify({
                    "message": "Login successful!",
                    "token": token,
                    "user": {
                        "id": user_id,
                        "email": user_email,
                        "username": username,
                        "roles": roles,
                        "ownername": ownername if is_worker else "N/A"
                    }
                }), 200
            else:
                return jsonify({"error": "Invalid credentials!"}), 401
        else:
            return jsonify({"error": "User not found!"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500 