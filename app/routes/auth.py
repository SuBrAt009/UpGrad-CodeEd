from flask import Blueprint, request, jsonify, make_response, g
from passlib.hash import argon2
from models import db, User
from utils.auth_middleware import issue_jwt, set_session_cookie, clear_session_cookie, auth_required

bp = Blueprint("auth", __name__)

def require_json(*fields):
    data = request.get_json(silent=True) or {}
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return None, (jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400)
    return data, None

@bp.post("/register")
def register():
    data, err = require_json("email", "password")
    if err: return err
    email = data["email"].strip().lower()
    password = data["password"]

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(email=email, password_hash=argon2.hash(password), name=data.get("name"))
    db.session.add(user)
    db.session.commit()

    token = issue_jwt(user.id)
    resp = make_response({"user": user.to_public()})
    return set_session_cookie(resp, token)

@bp.post("/login")
def login():
    data, err = require_json("email", "password")
    if err: return err
    email = data["email"].strip().lower()
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if not user or not argon2.verify(password, user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    from datetime import datetime as dt
    user.last_login_at = dt.utcnow()
    db.session.commit()

    token = issue_jwt(user.id)
    resp = make_response({"user": user.to_public()})
    return set_session_cookie(resp, token)

@bp.post("/logout")
def logout():
    resp = make_response({"ok": True})
    return clear_session_cookie(resp)

@bp.get("/me")
@auth_required
def me():
    return jsonify({"user": g.user.to_public()})
