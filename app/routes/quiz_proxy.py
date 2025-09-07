# app/routes/quiz_proxy.py
import os
import requests
from flask import Blueprint, request, Response, current_app

# FastAPI quiz engine base URL
QUIZ_BASE = os.getenv("QUIZ_BASE", "http://localhost:8001")

bp = Blueprint("quiz_proxy", __name__, url_prefix="/api/quiz")

# Headers to forward
FORWARD_HEADERS = {"authorization", "content-type", "cookie"}

def _forward(path: str):
    url = f"{QUIZ_BASE}{path}"
    headers = {k: v for k, v in request.headers if k.lower() in FORWARD_HEADERS}

    try:
        r = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            params=request.args,
            data=request.get_data(),
            timeout=15,
        )
    except requests.RequestException as e:
        current_app.logger.exception("Quiz proxy error")
        return Response(f"Upstream error: {e}", status=502)

    resp = Response(r.content, status=r.status_code)
    if "content-type" in r.headers:
        resp.headers["Content-Type"] = r.headers["content-type"]
    if "set-cookie" in r.headers:
        resp.headers["Set-Cookie"] = r.headers["set-cookie"]
    return resp

# --- Map the quiz endpoints ---
@bp.route("/session/start", methods=["POST", "OPTIONS"])
def qp_start(): return _forward("/session/start")

@bp.route("/session/next", methods=["POST", "OPTIONS"])
def qp_next(): return _forward("/session/next")

@bp.route("/session/hint", methods=["POST", "OPTIONS"])
def qp_hint(): return _forward("/session/hint")

@bp.route("/session/answer", methods=["POST", "OPTIONS"])
def qp_answer(): return _forward("/session/answer")

@bp.route("/session/explain_batch", methods=["POST", "OPTIONS"])
def qp_explain_batch(): return _forward("/session/explain_batch")
