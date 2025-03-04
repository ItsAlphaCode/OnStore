from flask import Flask
from backend.models import db
from backend.routes import create_api_blueprint, create_web_blueprint
from backend.admin import init_admin
from backend.admin_routes import custom_admin  # changed import
import os

def create_app():
    # Set the correct template folder to point to frontend/templates
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_path = os.path.join(base_dir, 'frontend', 'templates')
    static_path = os.path.join(base_dir, 'frontend', 'static')  # new static folder path
    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
    
    # Set a unique secret key so that session and flash work
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(create_api_blueprint(), url_prefix='/api')
    app.register_blueprint(create_web_blueprint())
    app.register_blueprint(custom_admin)  # register custom admin blueprint
    
    # Initialize admin panel; accessible at the /admin URL by default.
    init_admin(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
