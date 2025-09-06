import uuid
import enum
import datetime as dt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserType(enum.Enum):
    student = "student"
    professional = "professional"

def uuid_str() -> str:
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=uuid_str)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), default=dt.datetime.utcnow)
    last_login_at = db.Column(db.DateTime(timezone=True))

    student_profile = db.relationship(
        "StudentProfile", back_populates="user",
        uselist=False, cascade="all,delete"
    )
    professional_profile = db.relationship(
        "ProfessionalProfile", back_populates="user",
        uselist=False, cascade="all,delete"
    )

    def to_public(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }

class StudentProfile(db.Model):
    __tablename__ = "student_profiles"
    # Enforce 1:1 by using user_id as PK
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), primary_key=True)
    degree = db.Column(db.String(120))
    specialization = db.Column(db.String(120))
    college = db.Column(db.String(200))
    interested_profession = db.Column(db.String(200))
    user = db.relationship("User", back_populates="student_profile")

class ProfessionalProfile(db.Model):
    __tablename__ = "professional_profiles"
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), primary_key=True)
    current_role = db.Column(db.String(200))
    organization = db.Column(db.String(200))
    interested_profession = db.Column(db.String(200))
    user = db.relationship("User", back_populates="professional_profile")

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.String(36), primary_key=True, default=uuid_str)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(400))
    level = db.Column(db.String(50))           # e.g., Beginner/Intermediate
    tags = db.Column(db.String(200))           # comma-separated for MVP

    def to_public(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "short_description": self.short_description,
            "level": self.level,
            "tags": self.tags.split(",") if self.tags else [],
        }