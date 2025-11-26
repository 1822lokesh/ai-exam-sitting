# app/routes/admin_leaves.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.authz import require_roles
from app.extensions import db
from app.models import LeaveRequest

bp = Blueprint("admin_leaves", __name__, url_prefix="/api/admin")

@bp.route("/leaves", methods=["GET"])
@jwt_required()
@require_roles("ADMIN")
def all_leaves():
    leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()
    return jsonify([
        {"id": l.id, "staff_id": l.staff_id, "reason": l.reason, "status": l.status, "created_at": l.created_at.isoformat()}
        for l in leaves
    ])

@bp.route("/leave/<int:leave_id>/status", methods=["PATCH"])
@jwt_required()
@require_roles("ADMIN")
def update_leave_status(leave_id):
    data = request.get_json()
    status = data.get("status")
    if status not in {"APPROVED", "REJECTED"}:
        return jsonify({"error": "status must be APPROVED or REJECTED"}), 400
    lr = LeaveRequest.query.get_or_404(leave_id)
    lr.status = status
    db.session.commit()
    return jsonify({"message": "Leave status updated", "id": lr.id, "status": lr.status})