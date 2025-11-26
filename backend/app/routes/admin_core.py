from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.exam import Exam, Room
from app.models.user import User
from flask_jwt_extended import jwt_required
from app.utils.authz import require_roles   # ✅ import role checker

bp = Blueprint("admin_core", __name__, url_prefix="/api/admin")  # ✅ unique name

# ✅ Create Exam
@bp.route("/exam", methods=["POST"])
@jwt_required()
@require_roles("ADMIN")
def create_exam():
    data = request.get_json()
    exam = Exam(
        subject=data["subject"],
        semester=data["semester"],
        date=data["date"],
        start_time=data["start_time"],
        end_time=data["end_time"]
    )
    db.session.add(exam)
    db.session.commit()
    return jsonify({"message": "Exam created successfully"}), 201

# ✅ List Exams
@bp.route("/exams", methods=["GET"])
@jwt_required()
@require_roles("ADMIN")
def list_exams():
    exams = Exam.query.all()
    return jsonify([
        {
            "id": e.id,
            "subject": e.subject,
            "semester": e.semester,
            "date": str(e.date),
            "start_time": str(e.start_time),
            "end_time": str(e.end_time)
        } for e in exams
    ])

# ✅ Add Room
@bp.route("/room", methods=["POST"])
@jwt_required()
@require_roles("ADMIN")
def add_room():
    data = request.get_json()
    room = Room(
        name=data["name"],
        benches_count=data["benches_count"],
        capacity=data["capacity"]
    )
    db.session.add(room)
    db.session.commit()
    return jsonify({"message": "Room added successfully"}), 201

# ✅ List Students
@bp.route("/students", methods=["GET"])
@jwt_required()
@require_roles("ADMIN")
def list_students():
    students = User.query.filter_by(role="STUDENT").all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "branch": s.branch,
            "year": s.year
        } for s in students
    ])