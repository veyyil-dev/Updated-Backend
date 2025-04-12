from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists (local development)
if os.path.exists('.env'):
    load_dotenv()

# Flask app initialization
app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": os.getenv("CORS_ORIGINS", "*")}}, supports_credentials=True)

# Configuration
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "UserAdmin")
app.config['DATABASE_URL'] = os.getenv("DATABASE_URL", "postgres://neondb_owner:npg_js3X0AMyPHCq@ep-gentle-bar-a1814m6n-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")

# Import routes after app creation to avoid circular imports
from app.routes import api 