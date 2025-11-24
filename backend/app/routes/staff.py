from flask import Blueprint, jsonify

bp = Blueprint("staff", __name__)

@bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Staff blueprint working"})