from flask import Blueprint, jsonify
from app.models.exam import Exam
from app.models.allocation import Allocation
from app.models.user import User
from app.models.seat import Seat
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("student", __name__)

# ✅ View Exam Schedule
@bp.route("/exams", methods=["GET"])
@jwt_required()
def view_exams():
    exams = Exam.query.all()
    return jsonify([{
        "id": e.id,
        "subject": e.subject,
        "semester": e.semester,
        "date": str(e.date),
        "start_time": str(e.start_time),
        "end_time": str(e.end_time)
    } for e in exams])

# ✅ View Seat Allocation
@bp.route("/allocation", methods=["GET"])
@jwt_required()
def view_allocation():
    email = get_jwt_identity()
    student = User.query.filter_by(email=email).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    allocation = Allocation.query.filter_by(student_id=student.id).first()
    if not allocation:
        return jsonify({"message": "No seat allocated yet"}), 404

    # Fetch seat details
    seat = Seat.query.get(allocation.seat_id)

    return jsonify({
        "exam_id": allocation.exam_id,
        "room_id": allocation.room_id,
        "seat_id": allocation.seat_id,
        "seat_number": seat.seat_number if seat else None
    })