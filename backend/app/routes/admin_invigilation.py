# app/routes/admin_invigilation.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.authz import require_roles
from app.extensions import db
from app.models import Invigilation

bp = Blueprint("admin_invigilation", __name__, url_prefix="/api/admin")

@bp.route("/invigilation", methods=["POST"])
@jwt_required()
@require_roles("ADMIN")
def assign_invigilator():
    data = request.get_json()
    required = ["exam_id", "room_id", "staff_id"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    inv = Invigilation(
        exam_id=data["exam_id"],
        room_id=data["room_id"],
        staff_id=data["staff_id"]
    )
    db.session.add(inv)
    db.session.commit()
    return jsonify({"message": "Invigilation assigned", "id": inv.id}), 201

@bp.route("/invigilations", methods=["GET"])
@jwt_required()
@require_roles("ADMIN")
def list_invigilations():
    invs = Invigilation.query.all()
    return jsonify([
        {"id": i.id, "exam_id": i.exam_id, "room_id": i.room_id, "staff_id": i.staff_id}
        for i in invs
    ])