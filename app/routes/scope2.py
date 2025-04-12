from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from app.utils.database import get_db_connection

scope2 = Blueprint('scope2', __name__)

@scope2.route("/Scope2save", methods=["POST"])
def Scope2save():
    try:
        data = request.get_json()
        print("Received Data:", data)

        userid = data.get("username")
        templatecontent = data.get("templatecontent")
        templatesave = json.dumps(data.get("templatesave"))
        templatesave_scope2 = json.dumps(data.get("templatesave_scope2"))
        created_by = data.get("username")
        date = datetime.today().strftime('%Y-%m-%d')
        modified_date = datetime.today().strftime('%Y-%m-%d')
        modified_by = created_by
        total_kg_co2 = 0
        goods_units = data.get("goods_units")

        connection = get_db_connection()
        cursor = connection.cursor()

        check_query = "SELECT COUNT(*) FROM AllEntries WHERE userid = %s AND templatecontent = %s"
        cursor.execute(check_query, (userid, templatecontent))
        result = cursor.fetchone()

        if result[0] > 0:
            return jsonify({"error": "Template name already exists. Please choose a different name.", "message": False})

        cursor.execute('INSERT INTO AllEntries (userid, templatecontent, templatesave, "templateSave_scope2", created_by, date, modified_date, modified_by, total_kg_co2, goods_units) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                      (userid, templatecontent, templatesave, templatesave_scope2, created_by, date, modified_date, modified_by, total_kg_co2, goods_units))
        message = "New template saved successfully!"

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": message}), 200

    except Exception as e:
        print("Error saving Scope 2:", e)
        return jsonify({"error": str(e)}), 500

@scope2.route("/DataEntery/Scope2", methods=["POST"])
def DataEnteryScope2():
    try:
        data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert data into the database
        cursor.execute("""
            INSERT INTO scope2_data (user_id, data)
            VALUES (%s, %s)
        """, (data.get('user_id'), json.dumps(data.get('data'))))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Scope 2 data saved successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500 