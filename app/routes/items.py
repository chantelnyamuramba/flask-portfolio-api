import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, redis_client
from app.models import Item, User

items_bp = Blueprint('items', __name__)

CACHE_KEY_ALL_ITEMS = "items:all"
CACHE_TIMEOUT = 60  # Cache duration in seconds


@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    """Create a new item (Requires JWT Auth)."""
    current_user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    if not data.get('title') or data.get('price') is None:
        return jsonify({'error': 'Title and price are required'}), 400

    item = Item(
        title=data['title'],
        description=data.get('description', ''),
        price=float(data['price']),
        user_id=current_user_id
    )

    db.session.add(item)
    db.session.commit()

    # Invalidate cache so fresh data is loaded on next GET
    try:
        redis_client.delete(CACHE_KEY_ALL_ITEMS)
    except Exception:
        pass  # Fail gracefully if Redis is offline locally

    return jsonify({
        'message': 'Item created successfully',
        'item': item.to_dict()
    }), 201


@items_bp.route('/', methods=['GET'])
def get_items():
    """Retrieve all items with Redis caching."""
    # 1. Try fetching from Redis cache
    try:
        cached_data = redis_client.get(CACHE_KEY_ALL_ITEMS)
        if cached_data:
            return jsonify({
                'source': 'cache',
                'items': json.loads(cached_data)
            }), 200
    except Exception:
        pass  # Fallback to DB if Redis isn't running

    # 2. Cache miss: Query primary database
    items = Item.query.all()
    items_list = [item.to_dict() for item in items]

    # 3. Store result in Redis cache for 60 seconds
    try:
        redis_client.setex(CACHE_KEY_ALL_ITEMS, CACHE_TIMEOUT, json.dumps(items_list))
    except Exception:
        pass

    return jsonify({
        'source': 'database',
        'items': items_list
    }), 200


@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a single item by ID."""
    item = Item.query.get_or_404(item_id)
    return jsonify({'item': item.to_dict()}), 200


@items_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    """Delete an item (Owner or Admin only)."""
    current_user_id = int(get_jwt_identity())
    item = Item.query.get_or_404(item_id)

    user = User.query.get(current_user_id)

    # Authorization check
    if item.user_id != current_user_id and user.role != 'admin':
        return jsonify({'error': 'Unauthorized to delete this item'}), 403

    db.session.delete(item)
    db.session.commit()

    # Invalidate Redis cache
    try:
        redis_client.delete(CACHE_KEY_ALL_ITEMS)
    except Exception:
        pass

    return jsonify({'message': 'Item deleted successfully'}), 200