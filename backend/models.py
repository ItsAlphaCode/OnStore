from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    stores = relationship('Store', back_populates='category', lazy=True)
    
    def __repr__(self):
        return f"<Category {self.name}>"

class Store(db.Model):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    hours = Column(String(50), nullable=False)
    promotions_flag = Column(Boolean, default=False)
    store_type = Column(Boolean, default=False)
    description = Column(Text, nullable=False)
    location = Column(String(100), nullable=False)
    image_path = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = relationship('Category', back_populates='stores')
    
    def __repr__(self):
        return f"<Store {self.name}>"

class Promotion(db.Model):
    __tablename__ = 'promotions'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Promotion {self.title}>"

class Event(db.Model):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), index=True, nullable=False)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
class Product:
    pass
    
    def __repr__(self):
        return f"<Event {self.title}>"
    