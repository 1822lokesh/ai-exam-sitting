# app/routes/student_results.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Result

bp = Blueprint("student_results", __name__, url_prefix="/api/student")

# ✅ View own results
@bp.route("/results", methods=["GET"])
@jwt_required()
def my_results():
    email = get_jwt_identity()
    student = User.query.filter_by(email=email).first()
    results = Result.query.filter_by(student_id=student.id).all()
    return jsonify([
        {"exam_id": r.exam_id, "marks": r.marks, "grade": r.grade}
        for r in results
    ])

# ✅ View performance summary
@bp.route("/performance", methods=["GET"])
@jwt_required()
def my_performance():
    email = get_jwt_identity()
    student = User.query.filter_by(email=email).first()
    results = Result.query.filter_by(student_id=student.id).all()

    if not results:
        return jsonify({"message": "No results yet"}), 404

    total_marks = sum(r.marks for r in results)
    avg_marks = total_marks / len(results)

    return jsonify({
        "total_exams": len(results),
        "average_marks": avg_marks,
        "grades": [r.grade for r in results]
    })