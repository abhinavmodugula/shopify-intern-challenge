from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Warehouse(db.Model):
    __tablename__ = "warehouses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False, nullable=False)
    address = db.Column(db.Text, index=False, unique=False, nullable=True)



class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False, nullable=False)
    amount = db.Column(db.Integer, index=False, unique=False, nullable=False)
    value = db.Column(db.Integer, index=False, unique=False, nullable=False)
    notes = db.Column(db.Text, index=False, unique=False, nullable=True)
    date_created = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    warehouse_id = db.Column(db.Integer, ForeignKey('warehouses.id'), nullable=True)
    warehouse = relationship("Warehouse", backref="items", foreign_keys=[warehouse_id])
