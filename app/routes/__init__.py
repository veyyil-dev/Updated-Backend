from flask import Blueprint

# Import all route blueprints
from app.routes.auth import auth
from app.routes.scope1 import scope1
from app.routes.scope2 import scope2
from app.routes.dashboard import dashboard
from app.routes.templates import templates

# Create a main blueprint for all routes
api = Blueprint('api', __name__, url_prefix='/api')

# Register all blueprints
api.register_blueprint(auth, url_prefix='/auth')
api.register_blueprint(scope1, url_prefix='/scope1')
api.register_blueprint(scope2, url_prefix='/scope2')
api.register_blueprint(dashboard, url_prefix='/dashboard')
api.register_blueprint(templates, url_prefix='/templates')