from flask import Blueprint, jsonify

bp = Blueprint("student", __name__)

@bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Student blueprint working"})