import psycopg2
from flask import current_app

def get_db_connection():
    """Get a database connection using the configured DATABASE_URL."""
    connection = psycopg2.connect(current_app.config['DATABASE_URL'])
    return connection 