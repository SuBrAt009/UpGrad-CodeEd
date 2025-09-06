from flask import Blueprint, request, jsonify, g
from models import db, UserType, StudentProfile, ProfessionalProfile
from utils.auth_middleware import auth_required

bp = Blueprint("profile", __name__)

@bp.post("/college-student")
@auth_required
def upsert_student():
    body = request.get_json(silent=True) or {}
    g.user.user_type = UserType.student
    sp = g.user.student_profile or StudentProfile(user_id=g.user.id)
    sp.degree = body.get("degree")
    sp.specialization = body.get("specialization")
    sp.college = body.get("college")
    sp.interested_profession = body.get("interested_profession")
    db.session.add(sp)
    if g.user.professional_profile:
        db.session.delete(g.user.professional_profile)
    db.session.commit()
    return jsonify({"ok": True})

@bp.post("/working-professional")
@auth_required
def upsert_professional():
    body = request.get_json(silent=True) or {}
    g.user.user_type = UserType.professional
    pp = g.user.professional_profile or ProfessionalProfile(user_id=g.user.id)
    pp.current_role = body.get("current_role")
    pp.organization = body.get("organization")
    pp.interested_profession = body.get("interested_profession")
    db.session.add(pp)
    if g.user.student_profile:
        db.session.delete(g.user.student_profile)
    db.session.commit()
    return jsonify({"ok": True})
