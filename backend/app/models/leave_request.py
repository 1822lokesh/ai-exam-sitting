# app/models/leave_request.py
from app.extensions import db
from datetime import datetime

class LeaveRequest(db.Model):
    __tablename__ = "leave_requests"

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="PENDING")  # PENDING, APPROVED, REJECTED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)