

# Requirements
Python 3.8+
Flask (pip install flask)
Flask-SQLAlchemy (pip install flask-sqlalchemy)
Flask-Migrate (pip install flask-migrate)
Flask-WTF (pip install flask-wtf)

# Usage
Navigate the Website: Use the navigation bar to explore stores, promotions, and events.
Search for Stores: Utilize the search bar to locate specific stores or products.

# INSTALLATION

# Set Up Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

# Install Dependencies
Ensure you have Python 3.8+ installed. Then, install the required packages:

# Configure the Database
python backend/create_db.py
python backend/seed_database.py

# Start the Application
python run.py

# Usage
Navigate the Website: Use the navigation bar to explore stores, promotions, and events.
Search for Stores: Utilize the search bar to locate specific stores or products.
Admin Panel: Log in to the admin panel at /admin-panel to update content