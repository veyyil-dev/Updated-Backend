from app import app
from app.routes import api
import os

# Register the API blueprint
app.register_blueprint(api)

# Set the port from environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

@app.route("/")
def index():
    return "API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)