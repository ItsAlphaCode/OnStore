# cSpell:ignore jsonify madmin orig
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from backend.models import db, Store, Category, Promotion, Event  # Adjust imports based on your models
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime
from backend.image_upload import save_uploaded_image

custom_admin = Blueprint('custom_admin', __name__, url_prefix='/admin-panel')


# Home page for the admin panel
@custom_admin.route('/')
def index():
    return render_template('madmin/index.html')  # Ensure you have this template


# Add a new store
@custom_admin.route('/add_store', methods=['GET', 'POST'])
def add_store():
    if request.method == 'POST':
        # Retrieve form fields for the store
        name = request.form.get('name')
        category_name = request.form.get('category')  # Get category by name
        hours = request.form.get('hours')
        promotions_flag = True if request.form.get('promotions_flag') == 'on' else False
        store_type = True if request.form.get('store_type') == 'on' else False
        description = request.form.get('description')
        location = request.form.get('location')
        # Use image upload if file provided
        image_field = request.files.get('image')
        if image_field:
            uploaded_image = save_uploaded_image(image_field)
            image_path = uploaded_image if uploaded_image else 'static/images/default_store.jpg'
        else:
            image_path = request.form.get('image_path') or 'static/images/default_store.jpg'

        # Fetch the category ID from the database
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            flash("Category does not exist. Please create it first.", "error")
            return redirect(url_for('custom_admin.add_store'))

        # Check if a store with this name in the same category already exists
        existing_store = Store.query.filter_by(name=name, category_id=category.id).first()
        if existing_store:
            flash("Store already exists in this category.", "error")
            return redirect(url_for('custom_admin.add_store'))

        new_store = Store(
            name=name,
            category_id=category.id,
            hours=hours,
            promotions_flag=promotions_flag,
            store_type=store_type,
            description=description,
            location=location,
            image_path=image_path
        )
        try:
            db.session.add(new_store)
            db.session.commit()
            flash("Store added successfully.", "success")
            return redirect(url_for('custom_admin.add_store'))
        except IntegrityError as e:
            db.session.rollback()
            # Log the actual error for debugging (remove detailed error in production)
            print("IntegrityError:", e)
            # Optionally flash the detailed error message for debugging:
            flash("An error occurred while adding the store: " + str(e.orig), "error")
            return redirect(url_for('custom_admin.add_store'))
    
    categories = Category.query.all()
    stores = Store.query.all()  # added inventory for stores
    return render_template('madmin/add.html',
                           categories=categories,
                           active_section='store',
                           stores=stores)


# List all stores
@custom_admin.route('/stores')
def stores():
    stores_list = Store.query.all()
    promotions = Promotion.query.all()
    events = Event.query.all()
    categories = Category.query.all()
    return render_template('madmin/stores.html',
                           stores=stores_list,
                           promotions=promotions,
                           events=events,
                           categories=categories)


# Edit an existing store
@custom_admin.route('/edit_store/<int:store_id>', methods=['GET', 'POST'])
def edit_store(store_id):
    store = Store.query.get_or_404(store_id)
    if request.method == 'POST':
        store.name = request.form.get('name')
        category_name = request.form.get('category')
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            flash("Category does not exist. Please create it first.", "error")
            return redirect(url_for('custom_admin.stores'))
        store.category_id = category.id
        store.hours = request.form.get('hours')
        store.promotions_flag = True if request.form.get('promotions_flag') == 'on' else False
        store.store_type = True if request.form.get('store_type') == 'on' else False
        store.description = request.form.get('description')
        store.location = request.form.get('location')
        file = request.files.get('image')
        if file and file.filename != "":
            new_image = save_uploaded_image(file)
            if new_image:
                store.image_path = new_image
        db.session.commit()
        flash("Store updated successfully.", "success")
        return redirect(url_for('custom_admin.stores'))
    return redirect(url_for('custom_admin.stores'))


# Delete a store
@custom_admin.route('/delete_store/<int:store_id>', methods=['GET', 'POST'])
def delete_store(store_id):
    store = Store.query.get_or_404(store_id)
    if request.method == 'POST':
        db.session.delete(store)
        db.session.commit()
        flash("Store deleted successfully.", "success")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=True, deleted_id=store.id)
        return redirect(url_for('custom_admin.stores'))
    
    # For GET requests, redirect to stores with a flash message since the confirm_delete template does not exist.
    flash("Delete confirmation is handled via the modal. Please use the delete function on the Stores page.", "error")
    return redirect(url_for('custom_admin.stores'))


# Manage categories
@custom_admin.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        # Add a new category
        name = request.form.get('name')
        if not name:
            flash("Category name is required.", "error")
            return redirect(url_for('custom_admin.categories'))
        new_category = Category(name=name)
        try:
            db.session.add(new_category)
            db.session.commit()
            flash("Category added successfully.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Category already exists.", "error")
        return redirect(url_for('custom_admin.stores'))

    all_categories = Category.query.all()
    cat_counts = [(cat.name, len(cat.stores)) for cat in all_categories]
    # Instead of rendering madmin/categories.html, render add.html with active_section='category'
    return render_template('madmin/stores.html',)


# Edit a Category
@custom_admin.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    cat = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        new_name = request.form.get('name')
        if not new_name:
            flash("Category name is required.", "error")
            return redirect(url_for('custom_admin.stores'))
        cat.name = new_name
        db.session.commit()
        flash("Category updated successfully.", "success")
        return redirect(url_for('custom_admin.stores'))
    return redirect(url_for('custom_admin.stores'))


@custom_admin.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    cat = Category.query.get_or_404(category_id)
    db.session.delete(cat)
    db.session.commit()
    flash("Category deleted successfully.", "success")
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
         return jsonify(success=True, deleted_id=cat.id)
    return redirect(url_for('custom_admin.stores'))


# Add a promotion
@custom_admin.route('/add_promotion', methods=['GET', 'POST'])
def add_promotion():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        valid_until_str = request.form.get('valid_until')
        if not title or not description or not valid_until_str:
            flash("All fields are required.", "error")
            return redirect(url_for('custom_admin.add_promotion'))
        try:
            valid_until = datetime.strptime(valid_until_str, "%Y-%m-%d")
        except ValueError:
            flash("Incorrect date format for Valid Until. Please use YYYY-MM-DD.", "error")
            return redirect(url_for('custom_admin.add_promotion'))
        
        new_promotion = Promotion(
            title=title,
            description=description,
            valid_until=valid_until
        )
        db.session.add(new_promotion)
        db.session.commit()
        flash("Promotion added successfully.", "success")
        return redirect(url_for('custom_admin.promotions'))
    
    categories_list = Category.query.all()
    cat_counts = [(cat.name, len(cat.stores)) for cat in categories_list]
    promotions = Promotion.query.all()  # added inventory for promotions
    return render_template('madmin/add.html',
                           categories=categories_list,
                           cat_counts=cat_counts,
                           active_section='promotion',
                           promotions=promotions)


# Edit a Promotion
@custom_admin.route('/edit_promotion/<int:promotion_id>', methods=['GET', 'POST'])
def edit_promotion(promotion_id):
    promo = Promotion.query.get_or_404(promotion_id)
    if request.method == 'POST':
        promo.title = request.form.get('title')
        promo.description = request.form.get('description')
        valid_until_str = request.form.get('valid_until')
        try:
            promo.valid_until = datetime.strptime(valid_until_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return redirect(url_for('custom_admin.promotions'))
        db.session.commit()
        flash("Promotion updated successfully.", "success")
        return redirect(url_for('custom_admin.stores'))
    return redirect(url_for('custom_admin.stores'))


# List all promotions
@custom_admin.route('/promotions')
def promotions():
    # Instead of a separate promotions template, render add.html with promotion section active
    categories_list = Category.query.all()
    cat_counts = [(cat.name, len(cat.stores)) for cat in categories_list]
    return render_template('madmin/add.html',
                           categories=categories_list,
                           cat_counts=cat_counts,
                           active_section='promotion')


@custom_admin.route('/delete_promotion/<int:promotion_id>', methods=['POST'])
def delete_promotion(promotion_id):
    promo = Promotion.query.get_or_404(promotion_id)
    db.session.delete(promo)
    db.session.commit()
    flash("Promotion deleted successfully.", "success")
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
         return jsonify(success=True, deleted_id=promo.id)
    return redirect(url_for('custom_admin.stores'))


# Add an event
@custom_admin.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form.get('title')
        event_date_str = request.form.get('event_date')
        location = request.form.get('location')
        description = request.form.get('description')
        if not title or not event_date_str or not location or not description:
            flash("All fields are required.", "error")
            return redirect(url_for('custom_admin.add_event'))
        try:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Incorrect date format. Please use YYYY-MM-DD.", "error")
            return redirect(url_for('custom_admin.add_event'))
        
        new_event = Event(
            title=title,
            event_date=event_date,
            location=location,
            description=description
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event added successfully.", "success")
        return redirect(url_for('custom_admin.events'))

    categories_list = Category.query.all()
    cat_counts = [(cat.name, len(cat.stores)) for cat in categories_list]
    events = Event.query.all()  # added inventory for events
    return render_template('madmin/add.html',
                           categories=categories_list,
                           cat_counts=cat_counts,
                           active_section='event',
                           events=events)


# Edit an Event
@custom_admin.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.location = request.form.get('location')
        event.description = request.form.get('description')
        event_date_str = request.form.get('event_date')
        try:
            event.event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return redirect(url_for('custom_admin.stores'))
        db.session.commit()
        flash("Event updated successfully.", "success")
        return redirect(url_for('custom_admin.stores'))
    return redirect(url_for('custom_admin.stores'))


# List all events
@custom_admin.route('/events')
def events():
    # Instead of a separate events template, redirect to add.html defaulting to event listing
    categories_list = Category.query.all()
    cat_counts = [(cat.name, len(cat.stores)) for cat in categories_list]
    return render_template('madmin/stores.html',
                           categories=categories_list,
                           cat_counts=cat_counts,
                           active_section='event')


@custom_admin.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully.", "success")
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
         return jsonify(success=True, deleted_id=event.id)
    return redirect(url_for('custom_admin.stores'))


# Add items
@custom_admin.route('/add_items', methods=['GET'])
def add_items():
    # Prepare variables for add.html (e.g., categories and cat_counts)
    categories_list = Category.query.all()
    cat_counts = [(cat.name, len(cat.stores)) for cat in categories_list]
    stores = Store.query.all()
    promotions = Promotion.query.all()
    events = Event.query.all()
    return render_template('madmin/add.html',
                           categories=categories_list,
                           cat_counts=cat_counts,
                           stores=stores,
                           promotions=promotions,
                           events=events)


# Logout endpoint
@custom_admin.route('/logout')
def logout():
    # Clear user session (adjust session keys as needed)
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('web.home'))
