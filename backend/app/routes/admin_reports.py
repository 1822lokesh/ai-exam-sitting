# app/routes/admin_reports.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils.authz import require_roles
from app.models import User, Exam, Room, Seat, Allocation, Invigilation, LeaveRequest, Result
from sqlalchemy import func
from app.extensions import db

bp = Blueprint("admin_reports", __name__, url_prefix="/api/admin")

@bp.route("/reports", methods=["GET"])
@jwt_required()
@require_roles("ADMIN")
def reports():
    total_students = User.query.filter_by(role="STUDENT").count()
    total_staff = User.query.filter_by(role="STAFF").count()
    total_exams = Exam.query.count()
    total_rooms = Room.query.count()
    total_seats = Seat.query.count()
    total_allocations = Allocation.query.count()

    leaves_pending = LeaveRequest.query.filter_by(status="PENDING").count()
    leaves_approved = LeaveRequest.query.filter_by(status="APPROVED").count()
    leaves_rejected = LeaveRequest.query.filter_by(status="REJECTED").count()

    avg_marks = db.session.query(func.avg(Result.marks)).scalar() or 0
    grade_counts = db.session.query(Result.grade, func.count(Result.id)).group_by(Result.grade).all()
    grade_summary = {grade: count for grade, count in grade_counts}

    return jsonify({
        "students": total_students,
        "staff": total_staff,
        "exams": total_exams,
        "rooms": total_rooms,
        "seats": total_seats,
        "allocations": total_allocations,
        "leaves": {
            "pending": leaves_pending,
            "approved": leaves_approved,
            "rejected": leaves_rejected
        },
        "results": {
            "average_marks": avg_marks,
            "grade_distribution": grade_summary
        }
    })