# app/routes/staff.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.extensions import db
from app.models import Invigilation, LeaveRequest

bp = Blueprint("staff", __name__, url_prefix="/api/staff")

def current_user_id():
    claims = get_jwt()
    return claims.get("user_id")

@bp.route("/invigilations", methods=["GET"])
@jwt_required()
def my_invigilations():
    staff_id = current_user_id()
    invs = Invigilation.query.filter_by(staff_id=staff_id).all()
    return jsonify([
        {"id": i.id, "exam_id": i.exam_id, "room_id": i.room_id}
        for i in invs
    ])

@bp.route("/leave", methods=["POST"])
@jwt_required()
def apply_leave():
    staff_id = current_user_id()
    data = request.get_json()
    reason = data.get("reason")
    if not reason:
        return jsonify({"error": "reason is required"}), 400
    lr = LeaveRequest(staff_id=staff_id, reason=reason, status="PENDING")
    db.session.add(lr)
    db.session.commit()
    return jsonify({"message": "Leave request submitted", "id": lr.id}), 201

@bp.route("/leaves", methods=["GET"])
@jwt_required()
def my_leaves():
    staff_id = current_user_id()
    leaves = LeaveRequest.query.filter_by(staff_id=staff_id).all()
    return jsonify([
        {"id": l.id, "reason": l.reason, "status": l.status, "created_at": l.created_at.isoformat()}
        for l in leaves
    ])