# app/routes/staff_reports.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Invigilation, LeaveRequest

bp = Blueprint("staff_reports", __name__, url_prefix="/api/staff")

@bp.route("/reports", methods=["GET"])
@jwt_required()
def staff_reports():
    email = get_jwt_identity()
    staff = User.query.filter_by(email=email).first()

    inv_count = Invigilation.query.filter_by(staff_id=staff.id).count()
    leaves = LeaveRequest.query.filter_by(staff_id=staff.id).all()
    leaves_summary = {
        "total": len(leaves),
        "approved": sum(1 for l in leaves if l.status == "APPROVED"),
        "rejected": sum(1 for l in leaves if l.status == "REJECTED"),
        "pending": sum(1 for l in leaves if l.status == "PENDING"),
    }

    return jsonify({
        "invigilations": inv_count,
        "leaves": leaves_summary
    })