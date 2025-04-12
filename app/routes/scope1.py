from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from app.utils.database import get_db_connection

scope1 = Blueprint('scope1', __name__)

@scope1.route('/scope_factors', methods=['GET'])
def scope_factors():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT scope_factors FROM master ORDER BY scope_factors;")
    categories = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(categories)

@scope1.route('/saveScope1', methods=['POST', 'OPTIONS'])
def save_scope1():
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
        print("goods_units", goods_units)

        connection = get_db_connection()
        cursor = connection.cursor()

        check_query = "SELECT COUNT(*) FROM AllEntries WHERE userid = %s AND templatecontent = %s"
        cursor.execute(check_query, (userid, templatecontent))
        result = cursor.fetchone()

        print("Result:", result)

        if result[0] > 0:
            return jsonify({"error": "Template name already. Please choose a different name.", "message": False})

        cursor.execute('INSERT INTO AllEntries (userid, templatecontent, templatesave, "templateSave_scope2", created_by, date, modified_date, modified_by, total_kg_co2, goods_units) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                      (userid, templatecontent, templatesave, templatesave_scope2, created_by, date, modified_date, modified_by, total_kg_co2, goods_units))
        message = "New template saved successfully!"

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": message}), 200

    except Exception as e:
        print("Error saving Scope 1:", e)
        return jsonify({"error": str(e)}), 500

@scope1.route("/scope_activities/<path:checkedValuesScopeOne>", methods=["GET"])
def get_types(checkedValuesScopeOne):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Split the checked values and create a parameter list
        checked_values = checkedValuesScopeOne.split(',')
        placeholders = ','.join(['%s'] * len(checked_values))
        
        query = f"""
        SELECT DISTINCT scope_activities 
        FROM master 
        WHERE scope_factors IN ({placeholders})
        ORDER BY scope_activities;
        """
        
        cursor.execute(query, checked_values)
        activities = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return jsonify(activities)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 