from app.extensions import db

class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Room {self.name} capacity={self.capacity}>"