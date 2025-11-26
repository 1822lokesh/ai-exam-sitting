from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Allocation

bp = Blueprint("admin_allocations", __name__, url_prefix="/api/admin")

@bp.route("/allocation", methods=["POST"])
def create_allocation():
    data = request.get_json()

    # Minimal validation (expand later)
    required = ["exam_id", "room_id", "seat_id", "student_id"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    alloc = Allocation(
        exam_id=data["exam_id"],
        room_id=data["room_id"],
        seat_id=data["seat_id"],
        student_id=data["student_id"],
    )
    db.session.add(alloc)
    db.session.commit()
    return jsonify({"message": "Allocation created", "id": alloc.id}), 201

@bp.route("/allocations", methods=["GET"])
def list_allocations():
    allocations = Allocation.query.all()
    return jsonify([
        {
            "id": a.id,
            "exam_id": a.exam_id,
            "room_id": a.room_id,
            "seat_id": a.seat_id,
            "student_id": a.student_id
        } for a in allocations
    ])