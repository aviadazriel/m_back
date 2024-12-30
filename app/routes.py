from flask import Blueprint, request, jsonify
from .models import db, Item
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@main.route('/aviad')
def aviad():
    return jsonify({"message": "aviad test"})

# CRUD Operations
@main.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@main.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())

@main.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@main.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.json
    item.name = data['name']
    item.description = data.get('description')
    db.session.commit()
    return jsonify(item.to_dict())

@main.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200

# File Upload
@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filepath = os.path.join(request.app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded", "file_path": filepath})
