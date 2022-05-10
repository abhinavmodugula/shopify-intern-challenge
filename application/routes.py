from datetime import datetime
from .models import db, Item, Warehouse
from flask import render_template, request, flash, redirect, url_for, session, g, Blueprint

"""
This defines the backend for the website.

"""

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder="templates",
    static_folder="static"
)


# TODO: two more methods 1) general all items 2) get all items from one warehouse

@main_bp.route("/", methods=['GET'])
def hello():
    return items()

@main_bp.route("/items", methods=['GET'])
def items():
    all_items = Item.query.all()
    warehouses = Warehouse.query.all()
    return render_template("items.html", items=all_items, warehouses=warehouses)


@main_bp.route("/items/<int:warehouse_id>", methods=['GET'])
def items_by_warehouse(warehouse_id):
    all_items = Item.query.all()
    selected_items = []
    for item in all_items:
        if item.warehouse_id == warehouse_id:
            selected_items.append(item)
    warehouses = Warehouse.query.all()
    return render_template("curr_warehouse.html", items=selected_items, warehouses=warehouses, curr_house=warehouse_id)


@main_bp.route("/categorize_item/<int:item_id>/<int:warehouse_id>")
def cat_item(item_id, warehouse_id):
    item = Item.query.filter_by(id=item_id).first()
    warehouse = Warehouse.query.filter_by(id=warehouse_id).first()
    item.warehouse_id = warehouse_id
    item.warehouse = warehouse
    db.session.commit()
    return redirect(url_for("main_bp.items"))


@main_bp.route("/items/updateItem/<int:item_id>", methods=['GET', 'POST'])
def update_item_info(item_id):
    if request.method == 'POST':
        name = request.form["name"]
        amount = request.form["amount"]
        value = request.form["value"]
        notes = request.form["notes"]
        item = Item.query.filter_by(id=item_id).first()
        if item is not None:
            item.name = name
            item.amount = int(amount)
            item.value = int(value)
            item.notes = notes
            db.session.commit()
        return redirect(url_for("main_bp.items"))
    return redirect(url_for("main_bp.items"))


@main_bp.route("/delete/<int:item_id>")
def delete(item_id):
    if item_id is not None:
        item = Item.query.filter_by(id=item_id).first()
    if item is not None:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('main_bp.items'))


@main_bp.route("/deleteWarehouse/<int:warehouse_id>")
def delete_cat(warehouse_id):
    cat = Warehouse.query.filter_by(id=warehouse_id).first()
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('main_bp.items'))


@main_bp.route("/items/createWarehouse", methods=['POST', 'GET'])
def create_warehouse():
    """
    GET:
    POST:
    """
    if request.method == 'POST':
        name = request.form['name']
        #addy = request.form['address']

        new_warehouse = Warehouse(name=name, address="")
        db.session.add(new_warehouse)
        db.session.commit()
        return redirect(url_for('main_bp.items'))
    return redirect(url_for('main_bp.items'))


@main_bp.route("/items/createItem", methods=['POST', 'GET'])
def create_item():
    """
    GET:
    POST:
    """

    if request.method == 'POST':
        name = request.form["name"]
        amount = request.form["amount"]
        value = request.form["value"]
        notes = request.form["notes"]

        # check if item already exists
        item_exists = False
        item = Item.query.filter_by(name=name).first()
        if item is not None:
            item_exists = True

        if item_exists:
            flash("An item with that name has already been created.")
        else:
            new_item = Item(name=name, amount=int(amount), value=int(value), notes=notes, date_created=datetime.now())
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for("main_bp.items"))
    return render_template("createitem.html")
