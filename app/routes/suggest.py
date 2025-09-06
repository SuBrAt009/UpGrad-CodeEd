from flask import Blueprint, jsonify, g
from utils.auth_middleware import auth_required
from models import db, UserType, Course

bp = Blueprint("suggest", __name__, url_prefix="/suggestions")

@bp.get("")
@auth_required
def get_suggestions():
    u = g.user

    # Default: nothing to suggest yet
    suggestions = []

    # --- MVP rule: Student + BE + Computer Science => OOPS course
    if u.user_type == UserType.student and u.student_profile:
        deg = (u.student_profile.degree or "").lower()
        spec = (u.student_profile.specialization or "").lower()
        if ("b.e" in deg or "be" in deg or "bachelor" in deg) and any(
            key in spec for key in ["computer science", "cs", "cse", "cs-and"]
        ):
            oops = Course.query.filter_by(slug="oops-101").first()
            if oops:
                suggestions.append(oops.to_public())

    return jsonify({"suggestions": suggestions})
