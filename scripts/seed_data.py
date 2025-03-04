import json
import os, sys

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import create_app
from backend.models import db, Store, StoreDirectoryEntry, Promotion, Event, Product

app = create_app()

# Path to data.json
data_path = os.path.join(BASE_DIR, 'database', 'data.json')

with open(data_path, 'r') as f:
    data = json.load(f)

with app.app_context():
    # Optionally clear existing data
    # db.drop_all()
    # db.create_all()
    
    # Populate Store model using the "search_data" which holds store details
    for item in data.get('search_data', []):
        store = Store(
            name = item.get('name'),
            category = item.get('category'),
            hours = item.get('hours'),
            promotions = item.get('promotions', False),
            store_type = item.get('store_type', False),
            description = item.get('description'),
            location = item.get('location'),
            image = item.get('image')
        )
        db.session.add(store)
    
    # Populate StoreDirectoryEntry from the "all" list in "store_directory"
    for entry in data.get('store_directory', {}).get('all', []):
        sde = StoreDirectoryEntry(
            name = entry.get('name'),
            category = entry.get('category'),
            location = entry.get('location'),
            description = entry.get('description')
        )
        db.session.add(sde)
    
    # Populate Promotion model using "promotions" list
    for promo in data.get('promotions', []):
        p = Promotion(
            title = promo.get('title'),
            description = promo.get('description'),
            valid_until = promo.get('valid_until'),
            image = promo.get('image')
        )
        db.session.add(p)
    
    # Populate Event model using "events" list
    for ev in data.get('events', []):
        e = Event(
            title = ev.get('title'),
            date = ev.get('date'),
            event_location = ev.get('event_location'),
            event_description = ev.get('event_description'),
            image = ev.get('image')
        )
        db.session.add(e)
    
    db.session.commit()
    print("Seed data has been populated.")
