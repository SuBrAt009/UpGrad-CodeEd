# main.py
# FastAPI service for the adaptive quiz engine

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import time

import quiz.adaptive_inheritance_quiz as engine

app = FastAPI(title="Adaptive Quiz Engine")

# CORS (dev: open; tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request models ----------
class StartReq(BaseModel):
    user_id: str
    topic: str = "inheritance oops"
    time_limit: int = 300
    max_q: int = 10
    ai: str = "auto"

class NextReq(BaseModel):
    user_id: str
    topic: str

class AnswerReq(BaseModel):
    user_id: str
    topic: str
    item_id: str
    choice_index: int
    hint_used: bool = False
    time_sec: Optional[float] = None

class HintReq(BaseModel):
    user_id: str
    topic: str
    item_id: str

class ExplainEntry(BaseModel):
    item_id: str
    item_text: str
    options: List[str]
    correct_index: int
    chosen_index: int
    hint_used: bool
    time_sec: float

class ExplainBatchReq(BaseModel):
    user_id: str
    topic: str
    entries: List[ExplainEntry]

# ---------- Startup ----------
@app.on_event("startup")
def boot():
    engine.TIME_LIMIT_SECONDS = 300
    engine.ITEM_BANK.clear()
    engine.CORRECT_MAP.clear()
    engine.seed_inheritance_fallback(per_band=10, topic="inheritance oops")
    engine.ensure_pool_size_exact(topic="inheritance oops", per_band=10)
    engine.AI = engine.AIClient(preferred="auto")

# ---------- Routes ----------
@app.post("/session/start")
def start(req: StartReq):
    s = engine.get_session_state(req.user_id, req.topic)
    s.start_ts = None
    s.ability = 0.0
    s.mastery = 0.0
    s.fatigue_score = 0
    s.curr_band = "E"
    s.last_served_band = None
    s.last_served_was_review = False
    s.asked_count = 0
    s.window.clear()
    s.acc_last5 = 0.0
    s.hint_window.clear()
    s.seen_item_ids.clear()
    s.wrong_subskill_counts.clear()
    s.h_wrong_streak = 0
    engine.TIME_LIMIT_SECONDS = req.time_limit
    engine.save_session_state(s)
    return {"ok": True}

@app.post("/session/next")
def next_item(req: NextReq):
    nxt = engine.next_item(req.user_id, req.topic)
    if isinstance(nxt, engine.EndSession):
        return {"end": True, "reason": nxt.reason}
    s = engine.get_session_state(req.user_id, req.topic)
    rem = max(0, int(engine.TIME_LIMIT_SECONDS - (time.time() - s.start_ts)))
    return {
        "end": False,
        "item": {
            "id": nxt.id,
            "difficulty": nxt.difficulty,
            "text": nxt.text,
            "options": nxt.options,
            "correct_index": nxt.correct_index,  # FE won't show this; used for batch explain payload
        },
        "time_left": rem
    }

@app.post("/session/hint")
def hint(req: HintReq):
    it = next((x for x in engine.ITEM_BANK if x.id == req.item_id), None)
    if not it:
        raise HTTPException(404, "Item not found")
    hint = engine.AI.generate_hint(it.text, it.options, it.subskill)
    return {"hint": hint}

@app.post("/session/answer")
def answer(req: AnswerReq):
    it = next((x for x in engine.ITEM_BANK if x.id == req.item_id), None)
    if not it:
        raise HTTPException(404, "Item not found")
    elapsed = float(req.time_sec or 0.0)
    if elapsed <= 0:
        elapsed = max(0.1, it.avg_time_sec)
    engine.record_response(req.user_id, req.topic, it, req.choice_index, elapsed, req.hint_used)
    s = engine.get_session_state(req.user_id, req.topic)
    return {
        "correct": (req.choice_index == it.correct_index),
        "correct_index": it.correct_index,
        "state": {
            "band": s.curr_band,
            "asked": s.asked_count,
            "ability": s.ability,
            "acc_last5": s.acc_last5,
            "fatigue": s.fatigue_score,
            "mastery": s.mastery
        }
    }

@app.post("/session/explain_batch")
def explain_batch(req: ExplainBatchReq):
    # Score purely from correctness in entries
    score = sum(1 for e in req.entries if e.chosen_index == e.correct_index)
    out = []
    for e in req.entries:
        exp = engine.AI.generate_explanation(e.item_text, e.options, e.correct_index, e.chosen_index)
        out.append({
            "item_id": e.item_id,
            "explanation": exp,
            "chosen_index": e.chosen_index,
            "correct_index": e.correct_index
        })
    s = engine.get_session_state(req.user_id, req.topic)
    label = engine.classify_by_score(score)
    return {
        "classification": label,
        "score": score,
        "asked": len(req.entries),
        "ability": s.ability,
        "mastery": s.mastery,
        "acc_last5": s.acc_last5,
        "fatigue": s.fatigue_score,
        "explanations": out
    }
