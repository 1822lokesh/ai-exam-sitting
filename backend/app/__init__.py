from flask import Flask
from .config import Config
from .extensions import db, migrate, mail, jwt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": app.config.get("FRONTEND_ORIGIN")}})

    # Import models so SQLAlchemy sees them
    from . import models   # this loads everything from app/models/__init__.py

    # Register blueprints
    from .routes import auth, admin_core, admin_rooms, admin_allocations, student, staff, admin_invigilation, admin_leaves, admin_results, student_results, admin_reports, staff_reports

   # Phase 3: only auth + admin_rooms
    app.register_blueprint(auth.bp, url_prefix="/api/auth")
    app.register_blueprint(admin_core.bp, url_prefix="/api/admin")
    app.register_blueprint(admin_rooms.bp, url_prefix="/api/admin")
    app.register_blueprint(admin_allocations.bp, url_prefix="/api/admin")
    app.register_blueprint(student.bp, url_prefix="/api/student")
    app.register_blueprint(admin_invigilation.bp, url_prefix="/api/admin")
    app.register_blueprint(admin_leaves.bp, url_prefix="/api/admin")
    app.register_blueprint(staff.bp, url_prefix="/api/staff")
    app.register_blueprint(admin_results.bp, url_prefix="/api/admin")
    app.register_blueprint(student_results.bp, url_prefix="/api/student")
    app.register_blueprint(admin_reports.bp, url_prefix="/api/admin")
    app.register_blueprint(staff_reports.bp, url_prefix="/api/staff")

    return app