from flask import Blueprint, request, jsonify
from app.utils.database import get_db_connection

templates = Blueprint('templates', __name__)

@templates.route('/', methods=['GET'])
def get_templates():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT DISTINCT templatecontent 
            FROM AllEntries 
            ORDER BY templatecontent
        """)
        
        templates = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return jsonify(templates), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@templates.route("/getTempnameToEditing", methods=["GET"])
def getTempnameToEditing():
    try:
        username = request.args.get("username")
        templatecontent = request.args.get("templatecontent")

        connection = get_db_connection()
        cursor = connection.cursor()

        # Select specific columns
        query = """
            SELECT id, templatecontent, templatesave ,"templateSave_scope2"
            FROM AllEntries 
            WHERE userid = %s AND templatecontent = %s
        """
        cursor.execute(query, (username, templatecontent))
        rows = cursor.fetchall()

        print("rows", rows)

        # Format the results into dictionaries
        entries = []
        for row in rows:
            entries.append({
                "id": row[0],
                "templatecontent": row[1],
                "templatesave": row[2],
                "templateSave_scope2": row[3]  
            })

        cursor.close()
        connection.close()

        return jsonify({"entries": entries}), 200

    except Exception as e:
        print("Error fetching entries:", e)
        return jsonify({"error": str(e)}), 500

@templates.route("/edit", methods=["GET"])
def get_templates_for_editing():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, templatecontent, templatesave, "templateSave_scope2"
            FROM AllEntries 
            ORDER BY date DESC
        """)
        
        entries = cursor.fetchall()
        
        formatted_entries = []
        for entry in entries:
            formatted_entries.append({
                'id': entry[0],
                'template_name': entry[1],
                'template_save': entry[2],
                'template_save_scope2': entry[3]
            })
        
        cursor.close()
        connection.close()
        
        return jsonify(formatted_entries), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@templates.route("/edit/<int:template_id>", methods=["GET"])
def get_template_for_edit(template_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, templatecontent, templatesave, "templateSave_scope2"
            FROM AllEntries 
            WHERE id = %s
        """, (template_id,))
        
        entry = cursor.fetchone()
        
        if not entry:
            return jsonify({"error": "Template not found"}), 404
            
        formatted_entry = {
            'id': entry[0],
            'template_name': entry[1],
            'template_save': entry[2],
            'template_save_scope2': entry[3]
        }
        
        cursor.close()
        connection.close()
        
        return jsonify(formatted_entry), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@templates.route('/', methods=['DELETE'])
def delete_template():
    try:
        data = request.get_json()
        template_name = data.get('template_name')
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM AllEntries WHERE templatecontent = %s", (template_name,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Template deleted successfully!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500