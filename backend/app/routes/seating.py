from flask import Blueprint, jsonify

bp = Blueprint("seating", __name__)

@bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Seating blueprint working"})