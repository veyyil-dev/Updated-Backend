from flask import Blueprint, request, jsonify
from app.utils.database import get_db_connection

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/DashBoardDataPost", methods=["POST"])
def DashBoardData():
    try:
        data = request.json  # Extract JSON data from request
        
        # Extract individual fields from JSON request
        record_date = data.get("record_date")
        username = data.get("username")
        goods_produced = data.get("goods_produced")
        co2_emitted = data.get("co2_emitted")
        goods_unit = data.get("goods_unit", "")  # Default to empty string if missing
        scope1 = data.get("scope1") 
        scope2 = data.get("scope2")
        shift = data.get("shift")
        template_id = int(data.get("template_Id"))

        print("tempalt",data)

        # Ensure all required fields are provided
        if None in [record_date, username, goods_produced, co2_emitted, scope1, scope2, shift,template_id,goods_unit]:
            return jsonify({"error": "Missing required fields"}), 400

        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert query
        query = """
        INSERT INTO dashboard_data 
        (record_date, username, goods_produced, co2_emitted, scope1, scope2, shift,template_id,goods_unit) 
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)
        """
        
        cursor.execute(query, (record_date, username, goods_produced, co2_emitted, scope1, scope2, shift,template_id,goods_unit))
        
        # Commit the transaction and close connection
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Data inserted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@dashboard.route('/DashBoard', methods=['GET'])
def getdashboarddata():
    connection = get_db_connection()
    cursor = connection.cursor()

    # ✅ Extract template_id from the query params
    template_id = request.args.get('Template_Id')

    if not template_id:
        return jsonify({"error": "Missing Template_Id parameter"}), 400

    try:
        # ✅ Fetch only the data for the specific template_id
        query = """
        SELECT 
            record_date, 
            goods_produced, 
            co2_emitted, 
            scope1, 
            scope2, 
            username, 
            shift, 
            record_id
        FROM dashboard_data
        WHERE template_id = %s
        """
        
        cursor.execute(query, (template_id,))
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        # ✅ Convert DB rows to JSON format
        data = [
            {
                "date": row[0].strftime('%Y-%m-%d'),  # Format date correctly
                "goodsProduced": row[1],
                "co2Emitted": row[2],
                "scope1": row[3],
                "scope2": row[4],
                "username": row[5],
                "shift": row[6],
                "record_id": row[7]
            }
            for row in rows
        ]

        return jsonify(data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

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