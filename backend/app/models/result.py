# app/models/result.py
from app.extensions import db

class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"<Result exam={self.exam_id} student={self.student_id} marks={self.marks} grade={self.grade}>"