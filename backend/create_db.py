__all__ = ['db_create']

import sys
import os

# Add the project root to sys.path so that "backend" can be imported
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import create_app
from backend.models import db

app = create_app()
def db_create():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

if __name__ == '__main__':
    db_create()
