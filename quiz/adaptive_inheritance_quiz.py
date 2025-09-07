# adaptive_inheritance_quiz.py
# Adaptive micro-quiz (MCQ) with:
# - Fixed pool size: 30 items (10 E, 10 M, 10 H) for the chosen topic
# - Ask only 10 questions; total session window = 300s
# - No repeats (seen_item_ids + enforced pool trimming)
# - E/M/H staircase; AI hints (on demand); AI explanations generated ONCE at the end (batch)
# - AI item generation optional; strict “inheritance” topic enforcement + curated fallback bank
# - Classification: SCORE-BASED (10=Excellent, 8–9=Good, 6–7=Average, ≤5=Poor)
# - Hint penalties are SMALL and consistent across mastery/accuracy/ability/fatigue

import os
import math
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# =========================
# Config
# =========================
TIME_LIMIT_SECONDS = 300      # total test window
FIXED_PER_BAND = 10           # EXACTLY 10 per difficulty -> 30 total pool

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
AI_TIMEOUT = 8
AI_RETRIES = 1
DEGRADE_ON_ERROR = True

# --- Hint sensitivity (small penalties) ---
HINT_CORRECT_MASTERY   = 0.90   # correct+hint mastery credit
HINT_WRONG_MASTERY     = 0.05   # wrong+hint mastery credit
HINT_CORRECT_ACCURACY  = 0.90   # correct+hint accuracy credit in last-5 window
HINT_WRONG_ACCURACY    = 0.10   # wrong+hint accuracy credit in last-5 window
HINT_ETA_MULTIPLIER    = 0.85   # ability LR damping if hint used
HINT_FATIGUE_RELAX_Z   = 2.0    # relax timing threshold for fatigue when hint used

# =========================
# AI client (OpenAI / Anthropic / Fallback)
# =========================
class AIClient:
    def __init__(self, preferred: str = "auto"):
        self.mode = "fallback"
        self.status = "ok"
        self.has_openai = False
        self.has_anthropic = False
        self._init_clients(preferred)

    def _init_clients(self, preferred: str):
        if preferred == "off":
            self.mode = "fallback"; return
        if preferred == "openai":
            if os.getenv("OPENAI_API_KEY"): self._try_init_openai(); return
            self.mode = "fallback"; return
        if preferred == "anthropic":
            if os.getenv("ANTHROPIC_API_KEY"): self._try_init_anthropic(); return
            self.mode = "fallback"; return
        if os.getenv("OPENAI_API_KEY"):
            if self._try_init_openai(): return
        if os.getenv("ANTHROPIC_API_KEY"):
            if self._try_init_anthropic(): return
        self.mode = "fallback"

    def _try_init_openai(self):
        try:
            from openai import OpenAI
            self.openai = OpenAI(timeout=AI_TIMEOUT)
            self.has_openai = True
            self.mode = "openai"
            return True
        except Exception as e:
            self.status = f"openai_init_error: {e}"
            return False

    def _try_init_anthropic(self):
        try:
            import anthropic
            self.anthropic = anthropic.Anthropic(timeout=AI_TIMEOUT)
            self.has_anthropic = True
            self.mode = "anthropic"
            return True
        except Exception as e:
            self.status = f"anthropic_init_error: {e}"
            return False

    def _degrade(self, e: Exception):
        if DEGRADE_ON_ERROR:
            self.status = f"degraded_to_fallback: {e}"
            self.mode = "fallback"

    # ---- low-level calls
    def _openai_call(self, system: str, user: str) -> str:
        for attempt in range(AI_RETRIES + 1):
            try:
                resp = self.openai.responses.create(
                    model=OPENAI_MODEL,
                    input=[{"role": "system", "content": system},
                           {"role": "user", "content": user}],
                )
                txt = getattr(resp, "output_text", None)
                if txt: return txt.strip()
                if hasattr(resp, "output") and resp.output:
                    piece = resp.output[0]
                    if hasattr(piece, "content") and piece.content:
                        block = piece.content[0]
                        if hasattr(block, "text"):
                            return block.text.strip()
                return ""
            except Exception as e:
                if attempt >= AI_RETRIES:
                    self._degrade(e); return ""
                time.sleep(0.3)

    def _anthropic_call(self, system: str, user: str) -> str:
        for attempt in range(AI_RETRIES + 1):
            try:
                resp = self.anthropic.messages.create(
                    model=ANTHROPIC_MODEL,
                    max_tokens=350,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                if resp and resp.content:
                    block = resp.content[0]
                    txt = getattr(block, "text", None)
                    return (txt or "").strip()
                return ""
            except Exception as e:
                if attempt >= AI_RETRIES:
                    self._degrade(e); return ""
                time.sleep(0.3)

    # ---- public helpers
    def generate_hint(self, stem: str, options: List[str], subskill: Optional[str]) -> str:
        system = ("Generate ONE short, actionable hint for a multiple-choice programming/OOP question. "
                  "Do NOT reveal the answer or option letter. Max 1 sentence.")
        user = f"Question: {stem}\nOptions: {options}\nSubskill/Concept: {subskill or 'inheritance'}\n"
        if self.mode == "openai":
            txt = self._openai_call(system, user)
            return txt or "Focus on which class defines/overrides the method in the inheritance chain."
        if self.mode == "anthropic":
            txt = self._anthropic_call(system, user)
            return txt or "Focus on which class defines/overrides the method in the inheritance chain."
        return "Check which class actually defines or overrides the attribute/method being accessed."

    def generate_explanation(self, stem: str, options: List[str], correct_idx: int, chosen_idx: int) -> str:
        system = ("You are a tutor. Give a 2–3 line explanation. "
                  "First, why the correct option is right; then one reason the chosen wrong option is misleading. "
                  "Be concise and concrete.")
        user = (f"Question: {stem}\nOptions: {options}\n"
                f"Correct option index: {correct_idx}\nStudent chose index: {chosen_idx}\n")
        if self.mode == "openai":
            txt = self._openai_call(system, user)
            return txt or self._fallback_expl(correct_idx, chosen_idx)
        if self.mode == "anthropic":
            txt = self._anthropic_call(system, user)
            return txt or self._fallback_expl(correct_idx, chosen_idx)
        return self._fallback_expl(correct_idx, chosen_idx)

    def _fallback_expl(self, correct_idx: int, chosen_idx: int) -> str:
        if chosen_idx == correct_idx:
            return "Correct: this aligns with how inheritance resolves methods/attributes along the base→subclass chain."
        return ("Correct option reflects the actual method resolution or override rules in the hierarchy. "
                "The chosen option ignores which class defines or overrides the behavior.")

    def generate_mcq(self, topic: str, difficulty: str, subskill: Optional[str]) -> Dict[str, object]:
        # Fallback-only or minimal AI; we have a robust offline bank anyway.
        stem, options, idx = get_inheritance_fallback_item_random(difficulty)
        return {"stem": stem, "options": options, "correct_index": idx, "subskill": subskill or "inheritance"}

# Initialized in main()
AI: "AIClient" = None

# =========================
# Validation & topic enforcement (kept simple; we use curated bank)
# =========================
def topic_keywords_for(topic: str) -> List[str]:
    t = topic.lower()
    if "inherit" in t:
        return ["inherit", "override", "polymorph", "mro", "base class", "subclass", "virtual"]
    return []

# =========================
# Inheritance fallback bank (≥12 per band; we sample 10)
# =========================
def _inheritance_bank():
    return {
        "E": [
            ("Which best describes inheritance in OOP?",
             ["A class acquiring properties/behavior of another","Compiling code to bytecode","Only data hiding","Linking external libraries"], 0),
            ("Single inheritance means a class inherits from:",
             ["Exactly one base class","Two unrelated classes","Any number of classes","Only interfaces/abstract types"], 0),
            ("Which feature allows a subclass to provide its own method body?",
             ["Overriding","Overloading","Encapsulation","Serialization"], 0),
            ("Which relationship signals inheritance?",
             ["is-a","has-a","uses-a","contains-a"], 0),
            ("Overriding occurs when:",
             ["Subclass defines same signature and replaces behavior","Two methods share name but different params","A private method is redefined","A static method is hidden"], 0),
            ("What is inherited by default?",
             ["Public/protected members (language-specific)","Private members directly","Local variables","Constructors"], 0),
            ("Polymorphism enables:",
             ["Base reference invoking subclass override","Subclass holding any base instance","Compile-time only behavior","Direct access to private base fields"], 0),
            ("Access modifier most restrictive for subclasses:",
             ["private","protected","public","internal"], 0),
            ("In Python, base listed first in C(B,A) affects:",
             ["MRO order","Constructor overloading","Static binding","Access modifiers"], 0),
            ("Which is NOT about inheritance?",
             ["Compiling to executable","Sharing behavior","Code reuse","Specialization"], 0),
            ("Abstract classes allow:",
             ["Defining template methods for subclasses","Instantiating directly","Only static members","Multiple constructors only"], 0),
            ("Interfaces express:",
             ["Contract for behavior across classes","Concrete state sharing","Private inheritance","File I/O rules"], 0),
        ],
        "M": [
            ("Class B extends A and overrides f(). What does B().f() call?",
             ["B.f (overridden in subclass)","A.f always","Both A.f then B.f automatically","Neither — unless super() is used"], 0),
            ("Which is TRUE about method overriding?",
             ["Same signature in subclass replaces base behavior at runtime","Requires a different return type","Only works on private methods","Happens at compile time"], 0),
            ("Polymorphism with collections works because:",
             ["A list of A can hold instances of subclasses of A","A list of B can hold A","Subclasses can hold bases","Only primitives are polymorphic"], 0),
            ("Calling super.f() in subclass does:",
             ["Invokes base implementation explicitly","Prevents overriding","Skips dynamic dispatch","Calls subclass method"], 0),
            ("Composition vs inheritance — prefer composition when:",
             ["You need has-a relationship and flexible reuse","You want is-a specialization","You need MRO","You need protected access"], 0),
            ("Which statement about protected members is typical?",
             ["Accessible in subclass but not by unrelated classes","Accessible everywhere","Hidden from subclass","Only for interfaces"], 0),
            ("Overloading vs overriding difference:",
             ["Overloading: same name diff params; overriding: same signature new impl","Overloading: runtime; overriding: compile-time","Overloading hides base","Overriding requires static"], 0),
            ("Dynamic dispatch means:",
             ["Call target resolved at runtime based on object type","Compiler chooses function at compile time","No virtual methods","Only static methods used"], 0),
            ("When might inheritance be harmful?",
             ["Tight coupling and fragile base-class problem","When using interfaces","When encapsulating variation","When doing dependency inversion"], 0),
            ("Liskov Substitution Principle implies:",
             ["Subtypes must be usable wherever supertypes are expected","Subtypes must expose all fields","Subtypes must be final","Only single inheritance allowed"], 0),
            ("In Python, super().__init__ is needed to:",
             ["Initialize base state explicitly in subclass","Disable overriding","Change MRO","Hide base attributes"], 0),
            ("In Java, @Override helps:",
             ["Catch signature mismatches at compile-time","Enable multiple inheritance","Create virtual methods","Access private base members"], 0),
        ],
        "H": [
            ("In Python, MRO (C3) for class C(A,B) typically resolves methods as:",
             ["C → A → B → object (consistent linearization)","C → B → A → object","A → B → C → object","Arbitrary at runtime"], 0),
            ("The ‘diamond problem’ is mitigated primarily by:",
             ["A defined method resolution order / virtual inheritance","Multiple dispatch by default","Compile-time templates","Name mangling of private members"], 0),
            ("In Java, which statement about inheritance is correct?",
             ["A class can extend one class and implement multiple interfaces","A class can extend multiple concrete classes","Private members are directly accessible to subclasses","Constructors are inherited"], 0),
            ("Fragile base-class arises when:",
             ["Changes in base break subclasses unexpectedly","Subclasses violate LSP","Multiple interfaces conflict","Static members override"], 0),
            ("Virtual inheritance in C++ solves:",
             ["Diamond duplication of base","Operator overloading","Template specialization","Name lookup ambiguity only"], 0),
            ("MRO linearization consistency requires:",
             ["Preserving local precedence order","Alphabetic class names","Depth-first search","Breadth-first search"], 0),
            ("Sealed/final classes affect inheritance by:",
             ["Preventing further subclassing","Forcing multiple inheritance","Allowing private overriding","Disabling constructors"], 0),
            ("Covariant returns in overriding allow:",
             ["Subclass method to return subtype of base method's return","Any unrelated type","Only exact same type","Primitives only"], 0),
            ("Mixins are typically used to:",
             ["Inject reusable behavior orthogonally","Provide single concrete base","Replace composition","Break encapsulation"], 0),
            ("Method hiding (static) differs from overriding because:",
             ["Binding is static; does not participate in dynamic dispatch","Binding is dynamic at runtime","It changes the vtable of instances","It guarantees polymorphism"], 0),
            ("Multiple inheritance risks:",
             ["Ambiguous bases and state duplication","Compile times","Garbage collection","Operator precedence"], 0),
            ("Subtype variance rules (e.g., PECS in Java) relate to:",
             ["Generics and inheritance boundaries","MRO only","Access modifiers","Serialization"], 0),
        ],
    }

def get_inheritance_fallback_item_random(band: str) -> Tuple[str, List[str], int]:
    bank = _inheritance_bank()
    band = band if band in bank else "E"
    return random.choice(bank[band])

# =========================
# Item model & bank
# =========================
@dataclass
class Item:
    id: str
    topic: str
    difficulty: str  # 'E' | 'M' | 'H'
    text: str
    options: List[str]
    correct_index: int
    avg_time_sec: float = 20.0
    sd_time_sec: float = 6.0
    subskill: Optional[str] = None
    hint: Optional[str] = None
    is_review: bool = False

ITEM_BANK: List[Item] = []
CORRECT_MAP: Dict[str, int] = {}

def add_item(topic: str, difficulty: str, stem: str, options: List[str], correct_index: int,
             subskill: Optional[str], avg_time: float, sd_time: float):
    # Shuffle options so correct answer isn't always A
    shuffled = options[:]
    random.shuffle(shuffled)
    new_correct_index = shuffled.index(options[correct_index])
    iid = f"{difficulty}-{topic}-{len(ITEM_BANK)}"
    it = Item(
        id=iid, topic=topic, difficulty=difficulty, text=stem,
        options=shuffled, correct_index=new_correct_index,
        avg_time_sec=avg_time, sd_time_sec=sd_time, subskill=subskill
    )
    ITEM_BANK.append(it)
    CORRECT_MAP[iid] = new_correct_index

def seed_inheritance_fallback(per_band: int, topic: str):
    bank = _inheritance_bank()
    for band in ("E", "M", "H"):
        pool = bank[band][:]
        random.shuffle(pool)
        for i in range(min(per_band, len(pool))):
            stem, options, idx = pool[i]
            add_item(
                topic=topic, difficulty=band,
                stem=f"[{band}] {stem}",
                options=options, correct_index=idx,
                subskill="inheritance",
                avg_time=(18 if band=='E' else 22 if band=='M' else 28),
                sd_time=(6 if band!='H' else 8)
            )

def ensure_pool_size_exact(topic: str, per_band: int = FIXED_PER_BAND):
    global ITEM_BANK
    new_bank: List[Item] = []
    by_band: Dict[str, List[Item]] = {'E': [], 'M': [], 'H': []}
    for it in ITEM_BANK:
        if it.topic == topic and it.difficulty in by_band:
            by_band[it.difficulty].append(it)
    for band in ('E','M','H'):
        lst = by_band[band]
        random.shuffle(lst)
        if len(lst) > per_band:
            lst = lst[:per_band]
        elif len(lst) < per_band:
            need = per_band - len(lst)
            fallback_pool = _inheritance_bank()[band][:]
            random.shuffle(fallback_pool)
            for i in range(need):
                stem, options, idx = fallback_pool[i % len(fallback_pool)]
                add_item(
                    topic=topic, difficulty=band,
                    stem=f"[{band}] {stem}",
                    options=options, correct_index=idx,
                    subskill="inheritance",
                    avg_time=(18 if band=='E' else 22 if band=='M' else 28),
                    sd_time=(6 if band!='H' else 8)
                )
            lst = [it for it in ITEM_BANK if it.topic == topic and it.difficulty == band]
            random.shuffle(lst)
            lst = lst[:per_band]
        new_bank.extend(lst)
    ITEM_BANK = new_bank

# =========================
# Session state & helpers
# =========================
@dataclass
class SessionState:
    user: str
    topic: str
    start_ts: Optional[float] = None
    ability: float = 0.0
    mastery: float = 0.0
    fatigue_score: int = 0
    curr_band: str = "E"
    last_served_band: Optional[str] = None
    last_served_was_review: bool = False
    asked_count: int = 0
    window: List[float] = field(default_factory=list)      # last-5 accuracy with partial credit
    acc_last5: float = 0.0
    hint_window: List[int] = field(default_factory=list)   # last-5 hint usage
    seen_item_ids: set = field(default_factory=set)
    wrong_subskill_counts: Dict[str, int] = field(default_factory=dict)
    h_wrong_streak: int = 0

SESSIONS: Dict[str, SessionState] = {}
def session_key(user, topic): return f"{user}::{topic}"
def get_session_state(user, topic) -> SessionState:
    key = session_key(user, topic)
    if key not in SESSIONS:
        SESSIONS[key] = SessionState(user=user, topic=topic)
    return SESSIONS[key]
def save_session_state(s: SessionState): SESSIONS[session_key(s.user, s.topic)] = s

B_MAP = {'E': -1.5, 'M': 0.0, 'H': 1.0}
def sigmoid(x: float) -> float: return 1.0 / (1.0 + math.exp(-x))
def now() -> float: return time.time()
def time_remaining(s: SessionState) -> float:
    if s.start_ts is None: return TIME_LIMIT_SECONDS
    return max(0.0, TIME_LIMIT_SECONDS - (now() - s.start_ts))

class EndSession:
    def __init__(self, reason: str): self.reason = reason

# =========================
# Classification (score-based)
# =========================
def classify_by_score(score: int) -> str:
    if score >= 10: return "Excellent"
    if 8 <= score <= 9: return "Good"
    if 6 <= score <= 7: return "Average"
    return "Poor"

# =========================
# Engine
# =========================
def pick_item(topic: str, difficulty: str, exclude_ids: Optional[set] = None) -> 'Item':
    pool = [it for it in ITEM_BANK if it.topic == topic and it.difficulty == difficulty and (exclude_ids is None or it.id not in exclude_ids)]
    if not pool:
        pool = [it for it in ITEM_BANK if it.topic == topic and (exclude_ids is None or it.id not in exclude_ids)]
    return random.choice(pool)

def next_item(user, topic):
    s = get_session_state(user, topic)
    if s.start_ts is None: s.start_ts = now()
    if time_remaining(s) <= 0: return EndSession("timeup")
    if s.fatigue_score >= 3:   return EndSession("fatigue")
    if s.asked_count >= 10:    return EndSession("max_q_reached")
    it = pick_item(topic, difficulty=s.curr_band, exclude_ids=s.seen_item_ids)
    s.asked_count += 1
    s.seen_item_ids.add(it.id)
    s.last_served_band = it.difficulty
    s.last_served_was_review = False
    save_session_state(s)
    return it

def record_response(user, topic, item: 'Item', chosen_index: int, time_sec: float, hint_used: bool = False):
    s = get_session_state(user, topic)
    b = B_MAP[item.difficulty]
    correct = (chosen_index == item.correct_index)

    # Ability (IRT-lite) with small hint damping
    p = sigmoid(s.ability - b)
    eta = 0.35
    eta_eff = eta * (HINT_ETA_MULTIPLIER if hint_used else 1.0)
    s.ability += eta_eff * ((1 if correct else 0) - p)

    # Fatigue (relaxed timing threshold if hint used)
    z = (time_sec - item.avg_time_sec) / max(1.0, item.sd_time_sec)
    z_threshold = HINT_FATIGUE_RELAX_Z if hint_used else 1.5
    if (z > z_threshold and not correct) or (s.acc_last5 <= 0.4 and len(s.window) >= 5):
        s.fatigue_score += 1
    else:
        s.fatigue_score = max(0, s.fatigue_score - 1)

    s.hint_window.append(1 if hint_used else 0)
    if len(s.hint_window) > 5: s.hint_window.pop(0)
    if sum(s.hint_window) >= 3 and len(s.hint_window) == 5:
        s.fatigue_score = min(3, s.fatigue_score + 1)

    # Rolling accuracy (partial credit)
    if correct and not hint_used:
        acc_credit = 1.0
    elif correct and hint_used:
        acc_credit = HINT_CORRECT_ACCURACY
    elif not correct and hint_used:
        acc_credit = HINT_WRONG_ACCURACY
    else:
        acc_credit = 0.0
    s.window.append(acc_credit)
    if len(s.window) > 5: s.window.pop(0)
    s.acc_last5 = sum(s.window) / len(s.window)

    # Mastery EWMA (partial credit)
    if correct and not hint_used:
        mastery_credit = 1.0
    elif correct and hint_used:
        mastery_credit = HINT_CORRECT_MASTERY
    elif not correct and hint_used:
        mastery_credit = HINT_WRONG_MASTERY
    else:
        mastery_credit = 0.0
    s.mastery = 0.7 * s.mastery + 0.3 * mastery_credit

    # Subskill mistakes
    if not correct and item.subskill:
        s.wrong_subskill_counts[item.subskill] = s.wrong_subskill_counts.get(item.subskill, 0) + 1

    # Staircase logic
    served = s.last_served_band or s.curr_band
    if served == 'E':
        s.curr_band = 'M' if correct else 'E'
        s.h_wrong_streak = 0
    elif served == 'M':
        if correct and not hint_used: s.curr_band = 'H'
        elif correct and hint_used:   s.curr_band = 'M'
        else:                         s.curr_band = 'E'
        s.h_wrong_streak = 0
    elif served == 'H':
        if correct:
            s.h_wrong_streak = 0; s.curr_band = 'H'
        else:
            s.h_wrong_streak += 1
            s.curr_band = 'M' if s.h_wrong_streak >= 2 else 'H'

    save_session_state(s)
