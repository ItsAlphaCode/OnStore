import json
import os
from backend.models import db, StoreDirectoryEntry
from your_app import app  # Adjust import as per your app factory pattern

with app.app_context():
    DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'database', 'data.json')
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    for entry in data.get("store_directory", {}).get("all", []):
        store_entry = StoreDirectoryEntry(
            name=entry.get("name"),
            category=entry.get("category"),
            location=entry.get("location"),
            description=entry.get("description")
        )
        db.session.add(store_entry)
    db.session.commit()
