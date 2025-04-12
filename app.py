from app import app
from app.routes import api

# Register the API blueprint
app.register_blueprint(api)





@app.route("/")
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)