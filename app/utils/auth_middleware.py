# utils/auth_middleware.py
import os, time, jwt
from functools import wraps
from datetime import datetime, timezone
from flask import request, jsonify, g
from sqlalchemy import or_

from models import User

# ---- Config (env-overridable) ----
JWT_SECRET = os.getenv("JWT_SECRET", "dev-super-secret-change-me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_TTL_HOURS = int(os.getenv("JWT_TTL_HOURS", "8"))

COOKIE_NAME = os.getenv("COOKIE_NAME", "session")
# For localhost HTTP dev, Secure=False and SameSite=Lax are fine.
# If you're on HTTPS and cross-site, use SameSite=None + Secure=True.
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")  # "Lax" | "None" | "Strict"
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"

# ---- Token issue/verify helpers ----
def issue_jwt(user_id: str) -> str:
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + JWT_TTL_HOURS * 3600,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def _decode_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])

def _load_user_from_claims(claims):
    sub = claims.get("sub") or claims.get("user_id") or claims.get("uid") or claims.get("email")
    if not sub:
        return None, "no subject (sub/user_id/email) in token"
    user = User.query.filter(or_(User.id == sub, User.email == sub)).first()
    if not user:
        return None, f"user not found for subject '{sub}'"
    return user, None

# ---- Cookie helpers ----
def set_session_cookie(resp, token: str):
    # Attach HttpOnly cookie so browser sends it automatically with credentials: "include"
    resp.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE,
        path="/",
    )
    return resp

def clear_session_cookie(resp):
    resp.delete_cookie(COOKIE_NAME, path="/")
    return resp

# ---- Auth middleware ----
def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Always allow CORS preflight
        if request.method == "OPTIONS":
            return ("", 200)

        # 1) Try Authorization header (Bearer or JWT)
        auth = request.headers.get("Authorization", "")
        if auth:
            try:
                scheme, tok = auth.split(" ", 1)
                if scheme.lower() in ("bearer", "jwt"):
                    claims = _decode_jwt(tok.strip())
                    exp = claims.get("exp")
                    if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                        return jsonify({"error": "token expired"}), 401
                    user, uerr = _load_user_from_claims(claims)
                    if uerr:
                        return jsonify({"error": uerr}), 401
                    g.user = user
                    return f(*args, **kwargs)
            except ValueError:
                return jsonify({"error": "malformed Authorization header"}), 401
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "token expired"}), 401
            except jwt.InvalidTokenError as e:
                return jsonify({"error": f"invalid token: {e}"}), 401

        # 2) Fallback to HttpOnly session cookie
        sess = request.cookies.get(COOKIE_NAME)
        if sess:
            try:
                claims = _decode_jwt(sess)
                user, uerr = _load_user_from_claims(claims)
                if uerr:
                    return jsonify({"error": uerr}), 401
                g.user = user
                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "session token expired"}), 401
            except jwt.InvalidTokenError as e:
                return jsonify({"error": f"invalid session token: {e}"}), 401

        # Nothing worked → clear reason helps in DevTools
        return jsonify({"error": "Unauthorized: no auth header or session cookie"}), 401
    return wrapper
