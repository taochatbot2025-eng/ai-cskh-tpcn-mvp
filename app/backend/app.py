from __future__ import annotations
import os
import json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from data_store import DataStore
from router import Router
from llm import generate_reply
from agent_intent import extract_intent
from agent_compose import compose_reply
import memory_store
import tools

load_dotenv()

APP_DIR = Path(__file__).parent.resolve()
DATA_DIR = os.getenv("DATA_DIR", str((APP_DIR / ".." / ".." / "data_kit" / "data").resolve()))
PROFILE_MODE = os.getenv("PROFILE_MODE", "SALES").upper()
AGENT_MODE = os.getenv("AGENT_MODE", "1").strip()  # "1"=agent on

def _cfg_dir():
    # Prefer config bundled with data_kit (data_kit/config) to keep repo root clean
    try:
        d = Path(DATA_DIR).resolve()
        dk = d.parent / "config"
        if dk.exists():
            return dk
    except Exception:
        pass
    # fallback: app/config
    return (APP_DIR.parent / "config")


def load_profile():
    cfg_dir = _cfg_dir()
    fname = "06_AI_PROFILE_SALES.json" if PROFILE_MODE == "SALES" else "06_AI_PROFILE_SOFT.json"
    return json.loads((cfg_dir / fname).read_text(encoding="utf-8"))

def load_router(alias_tags):
    cfg_dir = _cfg_dir()
    return Router.load(str(cfg_dir / "07_INTENT_ROUTER.json"), alias_tags)

app = Flask(__name__)
CORS(app)

store = DataStore.load(DATA_DIR)
profile = load_profile()
router = load_router(store.alias_tags)

def build_handoff(user_text: str, intent: str):
    # if intent is handoff-type OR routing keywords match
    if intent in ("kinh_doanh_dai_ly","khieu_nai","yeu_cau_cam_ket_ket_qua"):
        r = store.best_routing(user_text)
        return r
    # safety triggers => handoff if available
    if router.is_safety_trigger(user_text):
        r = store.best_routing(user_text) or store.best_routing("mang thai;cho con bú;dị ứng")
        return r
    return None

@app.get("/health")
def health():
    return {"ok": True, "profile": profile.get("profile_id"), "data_dir": DATA_DIR}

@app.post("/chat")
def chat():
    body = request.get_json(force=True, silent=True) or {}
    user_text = str(body.get("message", "")).strip()
    if not user_text:
        return jsonify({"reply": "Anh/chị cho em xin câu hỏi cụ thể để em hỗ trợ nhé 😊"}), 200

    # session id for memory (frontend may pass session_id; fallback to client ip)
    session_id = str(body.get("session_id") or request.headers.get("X-Session-Id") or request.remote_addr or "anon").strip()
    ctx = memory_store.get(session_id)
    turns = int(ctx.get("turns", 0) or 0)

    # ---- AGENT PIPELINE (default) ----
    if AGENT_MODE != "0":
        intent_json = extract_intent(user_text=user_text, ctx=ctx, meta=store.meta, profile_mode=PROFILE_MODE)

        # if previous turn asked clarify, merge user answer
        # (very lightweight: store pending_questions; agent will re-extract with ctx)
        if ctx.get("pending_clarify"):
            ctx.pop("pending_clarify", None)

        # need clarify => ask 1-2 smart questions
        if intent_json.get("need_clarify"):
            qs = intent_json.get("clarify_questions") or ["Anh/chị cho em biết mình đang cần hỗ trợ vấn đề gì ạ?"]
            memory_store.update(session_id, {
                "turns": turns + 1,
                "pending_clarify": True,
                "problem_key": intent_json.get("problem_key") or ctx.get("problem_key",""),
                "last_intent": intent_json.get("intent","unknown"),
                "tone": intent_json.get("tone","friendly"),
            })
            # Ask as 1 message (natural) — NO CTA in clarify turn
            reply = "Dạ em hỏi nhanh 1–2 ý để tư vấn đúng hơn ạ:\n- " + "\n- ".join(qs)
            return jsonify({"reply": reply, "topic": "general", "ctas": []}), 200

        # tool use
        intent = (intent_json.get("intent") or "unknown").strip()
        problem_key = (intent_json.get("problem_key") or ctx.get("problem_key") or "").strip()

        combos = []
        products = []
        faqs = []
        lead_saved = None

        # policy / FAQ
        if intent in ("buy_payment",):
            faqs = tools.tool_get_faq(store, "mua_hang_thanh_toan", limit=3) or tools.tool_get_faq(store, "mua_hang", limit=3)
        if intent in ("agency_policy","hard_business","complaint"):
            faqs = tools.tool_get_faq(store, "kinh_doanh_dai_ly", limit=3) or tools.tool_get_faq(store, "khieu_nai", limit=3)

        # combo/product retrieval
        if intent in ("combo","product"):
            if problem_key:
                combos = tools.tool_get_combo(store, problem_key, limit=2)
                if combos:
                    # expand products in combo
                    for c in combos:
                        products += tools.tool_get_combo_products(store, c)
                else:
                    products = tools.tool_search_products(store, problem_key, limit=4)

        # handoff decision (reuse existing)
        handoff = build_handoff(user_text, intent)

        # sales lead capture (soft) if signal and has phone in slots
        slots = intent_json.get("slots") or {}
        sales_signal = bool(intent_json.get("sales_signal"))
        if sales_signal and PROFILE_MODE == "SALES":
            phone = str(slots.get("phone","") or "").strip()
            if phone:
                lead_saved = tools.tool_save_lead(store.meta, {
                    "name": slots.get("name",""),
                    "phone": phone,
                    "area": slots.get("area",""),
                    "need": problem_key or intent
                })

        # compose
        reply = compose_reply(
            meta=store.meta,
            profile=profile,
            user_text=user_text,
            intent_json=intent_json,
            combos=combos,
            products=products,
            faqs=faqs,
            handoff=handoff,
            ctx={"turns": turns, "problem_key": problem_key, "last_intent": intent, "tone": intent_json.get("tone","friendly")},
            lead_saved=lead_saved
        )

        # contextual CTA (only when relevant)
        topic_key = _detect_topic_key(user_text, problem_key, intent)
        ctas = [c for c in (_contextual_cta(store.meta, topic_key) or []) if c]

        memory_store.update(session_id, {
            "turns": turns + 1,
            "problem_key": problem_key or ctx.get("problem_key",""),
            "last_intent": intent,
            "tone": intent_json.get("tone","friendly"),
        })
        return jsonify({"reply": reply, "topic": topic_key, "ctas": ctas}), 200

    # ---- FALLBACK (legacy router) ----
    intent, problem = router.classify(user_text)
    problem_key = problem or ""

    combos = []
    products = []
    faqs = []

    # flows (simplified implementation):
    if intent in ("huong_dan_mua_hang",):
        faqs = store.faq_by_intent("mua_hang", limit=3)
    elif intent in ("huong_dan_thanh_toan",):
        faqs = store.faq_by_intent("thanh_toan", limit=3)
    elif intent in ("chinh_sach_van_chuyen_doi_tra",):
        faqs = store.faq_by_intent("van_chuyen", limit=2) + store.faq_by_intent("doi_tra", limit=2)
    elif intent in ("tu_van_combo",):
        if not problem_key:
            # ask clarifying question without calling LLM
            return jsonify({"reply": "Dạ anh/chị đang muốn hỗ trợ vấn đề nào ạ (ví dụ: tiểu đường, dạ dày, mỡ máu, gan, xương khớp…)? 😊"}), 200
        combos = store.find_combos_by_problem(problem_key, limit=2)
        if combos:
            products = []
            for c in combos:
                products += store.expand_combo_products(c)
        else:
            products = store.find_products_by_problem(problem_key, limit=3)
            intent = "tu_van_san_pham"
    elif intent in ("tu_van_san_pham",):
        if not problem_key:
            return jsonify({"reply": "Dạ anh/chị đang gặp vấn đề nào để em gợi ý đúng (ví dụ: dạ dày, trào ngược, tiểu đường…)? 😊"}), 200
        products = store.find_products_by_problem(problem_key, limit=3)

    # handoff decision
    handoff = build_handoff(user_text, intent)

    # generate reply with LLM (natural language), constrained by context
    try:
        reply = generate_reply(profile=profile, meta=store.meta, intent=intent, user_text=user_text,
                               combos=combos, products=products, faqs=faqs, handoff=handoff)
    except Exception as e:
        # graceful fallback
        reply = "Dạ hệ thống đang bận một chút. Anh/chị cho em xin SĐT để bên em hỗ trợ nhanh qua hotline nhé ạ 😊"
    return jsonify({"reply": reply, "topic": topic_key, "ctas": ctas}), 200

# Serve frontend for quick demo (optional)
@app.get("/")
def index():
    return send_from_directory(str(APP_DIR.parent / "frontend"), "index.html")

@app.get("/<path:filename>")
def static_files(filename):
    return send_from_directory(str(APP_DIR.parent / "frontend"), filename)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
