# app/models/invigilation.py
from app.extensions import db

class Invigilation(db.Model):
    __tablename__ = "invigilations"

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # user with role=STAFF

    def __repr__(self):
        return f"<Invigilation exam={self.exam_id} room={self.room_id} staff={self.staff_id}>"