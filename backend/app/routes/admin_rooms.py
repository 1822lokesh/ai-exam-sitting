# app/routes/admin_rooms.py
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Room, Seat

bp = Blueprint("admin_rooms", __name__)

@bp.route("/rooms", methods=["POST"])
def create_room():
    data = request.get_json()
    room = Room(name=data["name"], capacity=data["capacity"])
    db.session.add(room)
    db.session.commit()
    return jsonify({"message": "Room created", "id": room.id}), 201

@bp.route("/rooms", methods=["GET"])
def list_rooms():
    rooms = Room.query.all()
    return jsonify([{"id": r.id, "name": r.name, "capacity": r.capacity} for r in rooms])

@bp.route("/seats", methods=["POST"])
def create_seat():
    data = request.get_json()
    seat = Seat(room_id=data["room_id"], seat_number=data["seat_number"])
    db.session.add(seat)
    db.session.commit()
    return jsonify({"message": "Seat created", "id": seat.id}), 201

@bp.route("/seats", methods=["GET"])
def list_seats():
    seats = Seat.query.all()
    return jsonify([{"id": s.id, "room_id": s.room_id, "seat_number": s.seat_number} for s in seats])