from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from backend.models import db, Store, Promotion, Event 

def init_admin(app):
    admin = Admin(
        app,
        name="Centerpoint Admin",
        template_mode="bootstrap3",
        base_template="madmin/master.html",
        url='/admin'
    )
    
    admin.add_view(ModelView(Store, db.session))
    admin.add_view(ModelView(Promotion, db.session))
    admin.add_view(ModelView(Event, db.session))
