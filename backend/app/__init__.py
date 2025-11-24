from flask import Flask
from .config import Config
from .extensions import db, migrate, mail, jwt, cors
from .routes import auth, admin, student, staff, seating

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
    from .models import user, exam, leave

    # Register blueprints
    app.register_blueprint(auth.bp, url_prefix="/api/auth")
    app.register_blueprint(admin.bp, url_prefix="/api/admin")
    app.register_blueprint(student.bp, url_prefix="/api/student")
    app.register_blueprint(staff.bp, url_prefix="/api/staff")
    app.register_blueprint(seating.bp, url_prefix="/api/seating")

    return app