from flask import Blueprint, request, jsonify
from app.utils.database import get_db_connection

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/data", methods=["POST"])
def dashboard_data():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT * FROM AllEntries 
            WHERE userid = %s 
            ORDER BY date DESC
        """, (user_id,))
        
        entries = cursor.fetchall()
        
        formatted_entries = []
        for entry in entries:
            formatted_entries.append({
                'id': entry[0],
                'template_name': entry[2],
                'date': entry[6],
                'total_co2': entry[9],
                'goods_units': entry[10]
            })
        
        cursor.close()
        connection.close()
        
        return jsonify(formatted_entries), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard.route('/data', methods=['GET'])
def get_dashboard_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT * FROM AllEntries 
            ORDER BY date DESC
        """)
        
        entries = cursor.fetchall()
        
        formatted_entries = []
        for entry in entries:
            formatted_entries.append({
                'id': entry[0],
                'user_id': entry[1],
                'template_name': entry[2],
                'date': entry[6],
                'total_co2': entry[9],
                'goods_units': entry[10]
            })
        
        cursor.close()
        connection.close()
        
        return jsonify(formatted_entries), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@dashboard.route('/DashBoardData', methods=['GET'])
def get_dashboard():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT record_date, goods_produced, co2_emitted, scope1, scope2, username, shift,record_id FROM dashboard_data")
    rows = cursor.fetchall()

    print(rows)

    cursor.close()
    connection.close()

    # Convert DB rows to required format
    data = [
        {   
            
            "date": row[0].strftime('%Y-%m-%d'),  # Format date correctly
            "goodsProduced": row[1],
            "co2Emitted": row[2],
            "scope1": row[3],
            "scope2": row[4],
            "username":row[5],
            "shift":row[6],
            "record_id":row[7]  
        }
        for row in rows
    ]

    return jsonify(data)

@dashboard.route('/data/<int:key>', methods=["PUT"])
def update_dashboard_data(key):
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            UPDATE AllEntries 
            SET templatecontent = %s,
                templatesave = %s,
                "templateSave_scope2" = %s,
                modified_date = CURRENT_DATE,
                modified_by = %s,
                total_kg_co2 = %s,
                goods_units = %s
            WHERE id = %s
        """, (
            data.get('template_name'),
            data.get('template_save'),
            data.get('template_save_scope2'),
            data.get('modified_by'),
            data.get('total_co2'),
            data.get('goods_units'),
            key
        ))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Data updated successfully!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard.route('/data/<int:key>', methods=["DELETE"])
def delete_dashboard_data(key):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM AllEntries WHERE id = %s", (key,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Data deleted successfully!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500