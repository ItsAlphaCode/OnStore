import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from backend.models import db, Store, Category, Promotion, Event, Product
from instance import db
from backend.image_upload import save_uploaded_image

# Add root directory to path for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define blueprints for user pages and APIs
web_bp = Blueprint('web', __name__)
api_bp = Blueprint('api', __name__)

# Context processors for global data
@web_bp.context_processor
def inject_categories():
    categories = Category.query.options(db.joinedload(Category.stores)).all()
    return dict(categories=categories)

@web_bp.context_processor
def inject_promotions():
    return dict(promotions=Promotion.query.filter(Promotion.valid_until >= datetime.now()).all())

@web_bp.context_processor
def inject_events():
    return dict(upcoming_events=Event.query.filter(Event.event_date >= datetime.now()).all())

# Home page
@web_bp.route('/')
def home():
    featured_stores = Store.query.filter_by(promotions_flag=True).limit(6).all()
    return render_template('home.html', featured_stores=featured_stores)

# About page
@web_bp.route('/about')
def about():
    return render_template('about.html')

# Contact page
@web_bp.route('/contact')
def contact():
    return render_template('contact.html')


# Search results page
@web_bp.route('/search-results')
def search_results():
    search_query = request.args.get('search', '').lower()
    category = request.args.get('category')
    filters = request.args.getlist('filter')  # get list of applied filters

    query = Store.query
    if search_query:
        query = query.filter(db.or_(
            Store.name.ilike(f"%{search_query}%"), 
            Store.description.ilike(f"%{search_query}%")
        ))
    if category:
        query = query.filter_by(category_id=category)
    # Additional filtering based on filter parameters
    if filters:
        if "Store Type" in filters:
            query = query.filter(Store.store_type == True)
        if "Promotions" in filters:
            query = query.filter(Store.promotions_flag == True)
    results = query.order_by(Store.name).all()
    return render_template('search_page.html', 
                           search_query=search_query,
                           search_data=results, 
                           selected_category=category)

# Store directory
@web_bp.route('/store-directory')
def store_directory():
    categories = Category.query.options(db.joinedload(Category.stores)).all()
    all_stores = []
    for category in categories:
        if category.stores:
            all_stores.extend(category.stores)
    return render_template('store_directory.html', categories=categories, all_stores=all_stores)

# Store details
@web_bp.route('/store/<int:store_id>')
def store_details(store_id):
    store = Store.query.get_or_404(store_id)
    return render_template('store_details.html', store=store)

# Promotions page
@web_bp.route('/promotions')
def promotions():
    promotions = Promotion.query.filter(Promotion.valid_until >= datetime.now()).all()
    expired_promotions = Promotion.query.filter(Promotion.valid_until < datetime.now()).all()
    return render_template('promotions.html', 
                           active_promotions=promotions,
                           expired_promotions=expired_promotions)

# Events page
@web_bp.route('/events')
def events():
    upcoming_events = Event.query.filter(Event.event_date >= datetime.now()).order_by(Event.event_date).all()
    past_events = Event.query.filter(Event.event_date < datetime.now()).order_by(Event.event_date.desc()).all()
    return render_template('events.html', 
                           upcoming_events=upcoming_events,
                           past_events=past_events)

# Careers page
@web_bp.route('/careers')
def careers():
    return render_template('careers.html')

# Parking page
@web_bp.route('/parking')
def parking():
    return render_template('parking.html')

# Removed admin panel related logic

def create_api_blueprint():
    return api_bp

def create_web_blueprint():
    return web_bp
