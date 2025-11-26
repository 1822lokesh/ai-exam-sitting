from app.extensions import db

class Seat(db.Model):
    __tablename__ = "seats"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    seat_number = db.Column(db.String(20), nullable=False)

    # Relationship back to Room
    room = db.relationship("Room", backref="seats", lazy=True)

    def __repr__(self):
        return f"<Seat {self.seat_number} in room {self.room_id}>"