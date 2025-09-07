import os
from flask import Flask
from flask_cors import CORS

from config import load_settings
from models import db, Course
from routes.auth import bp as auth_bp
from routes.profile import bp as profile_bp
from routes.suggest import bp as suggest_bp
from routes.quiz_proxy import bp as quiz_proxy_bp

def create_app():
    cfg = load_settings()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg["DB_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Allow your frontend to send/receive cookies (set FRONTEND_ORIGIN in .env for prod)
    CORS(
        app,
        resources={r"/api/*": {"origins": cfg["CORS_ORIGINS"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        # optional: expose headers you need the browser to read
        # expose_headers=["Content-Disposition"]
    )
    # Init DB and seed once
    db.init_app(app)
    with app.app_context():
        db.create_all()
        _seed_courses()

    # Register routes
    # in create_app()
    app.register_blueprint(auth_bp,    url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(suggest_bp, url_prefix="/api/suggestions")
    app.register_blueprint(quiz_proxy_bp)

    @app.get("/")
    def health():
        return {"ok": True}

    return app


def _seed_courses():
    """Idempotent seed for the MVP OOPS course."""
    if not Course.query.filter_by(slug="oops-101").first():
        db.session.add(
            Course(
                slug="oops-101",
                title="Object-Oriented Programming (OOPS) — Foundations",
                short_description=(
                    "Classes, objects, inheritance, polymorphism, and encapsulation "
                    "with hands-on quizzes."
                ),
                level="Beginner",
                tags="programming,oops,cs,foundations",
            )
        )
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
