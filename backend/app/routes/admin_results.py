# app/routes/admin_results.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.authz import require_roles
from app.extensions import db
from app.models import Result

bp = Blueprint("admin_results", __name__, url_prefix="/api/admin")

# ✅ Add result
@bp.route("/result", methods=["POST"])
@jwt_required()
@require_roles("ADMIN")
def add_result():
    data = request.get_json()
    required = ["exam_id", "student_id", "marks", "grade"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    result = Result(
        exam_id=data["exam_id"],
        student_id=data["student_id"],
        marks=data["marks"],
        grade=data["grade"]
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({"message": "Result added", "id": result.id}), 201

# ✅ List results for an exam
@bp.route("/results/<int:exam_id>", methods=["GET"])
@jwt_required()
@require_roles("ADMIN")
def list_results(exam_id):
    results = Result.query.filter_by(exam_id=exam_id).all()
    return jsonify([
        {"id": r.id, "student_id": r.student_id, "marks": r.marks, "grade": r.grade}
        for r in results
    ])