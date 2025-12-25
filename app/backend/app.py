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

# ---------- Contextual CTA helpers ----------
def _detect_topic_key(text: str) -> str:
    t = (text or "").lower()
    # digestive
    if any(k in t for k in ["dạ dày", "bao tử", "trào ngược", "đầy hơi", "ợ chua", "viêm loét"]):
        return "da_day"
    # diabetes / sugar
    if any(k in t for k in ["tiểu đường", "đường huyết", "huyết áp đường", "đái tháo đường"]):
        return "duong_huyet"
    # lipid
    if any(k in t for k in ["mỡ máu", "cholesterol", "triglycerid", "gan nhiễm mỡ"]):
        return "mo_mau"
    # joints
    if any(k in t for k in ["xương khớp", "khớp", "thoái hóa", "đau lưng", "gout"]):
        return "xuong_khop"
    # sleep
    if any(k in t for k in ["mất ngủ", "ngủ", "stress", "lo âu"]):
        return "giac_ngu"
    # buy / payment
    if any(k in t for k in ["mua", "đặt hàng", "thanh toán", "cod", "ship", "giao hàng", "đổi trả"]):
        return "mua_hang"
    # agency/business
    if any(k in t for k in ["đại lý", "cộng tác", "hoa hồng", "tuyến trên", "kinh doanh"]):
        return "kinh_doanh"
    return ""

def _detect_pronoun(text: str) -> str:
    t = (text or "").lower()
    if "chị" in t and "anh" not in t:
        return "chị"
    if "anh" in t and "chị" not in t:
        return "anh"
    return "anh/chị"

def build_contextual_ctas(meta: dict, topic_key: str, profile_mode: str, sales_signal: bool, turns: int) -> list:
    # CTA actions: send (prefill), link (open), handoff (open contact), order (send order intent)
    ctas = []
    # topic CTA
    topic_map = {
        "da_day": ("Xem combo dạ dày", "Đau dạ dày / trào ngược dùng combo nào?"),
        "duong_huyet": ("Xem combo đường huyết", "Người bị tiểu đường dùng combo nào?"),
        "mo_mau": ("Xem combo mỡ máu", "Mỡ máu cao dùng combo nào?"),
        "xuong_khop": ("Xem combo xương khớp", "Đau xương khớp dùng sản phẩm/combo nào?"),
        "giac_ngu": ("Xem giải pháp giấc ngủ", "Mất ngủ/lo âu nên dùng sản phẩm nào?"),
    }
    if topic_key in topic_map:
        label, payload = topic_map[topic_key]
        ctas.append({"label": label, "action": "send", "payload": payload})

    # purchase CTA appears only when meaningful (sales signal OR user asked buy OR turns>=1 and topic known)
    if profile_mode == "SALES" and (sales_signal or topic_key in ["mua_hang", "kinh_doanh"] or (turns >= 1 and topic_key)):
        ctas.append({"label": "Đặt nhanh", "action": "send", "payload": "Em muốn đặt hàng nhanh. Hướng dẫn em cách chốt đơn."})

    # handoff links appear when topic known or user is in buying flow
    if topic_key or sales_signal or turns >= 1:
        if meta.get("zalo"):
            ctas.append({"label": "Zalo 1-1", "action": "link", "url": str(meta.get("zalo"))})
        if meta.get("fanpage"):
            ctas.append({"label": "Fanpage", "action": "link", "url": str(meta.get("fanpage"))})
    return ctas


def detect_stage(user_text: str, intent_json: dict, turns: int, combos: list, products: list) -> str:
    """Heuristic stage for sales UX:
    - identify: chào hỏi / chưa rõ vấn đề / cần hỏi thêm
    - suggest: đã biết topic nhưng chưa đưa offer cụ thể
    - offer: đã đưa combo/sản phẩm cụ thể
    - close: user có tín hiệu mua/đặt hoặc đã để lại SĐT
    - support: mua hàng/thanh toán/chính sách
    """
    t = (user_text or "").lower()
    intent = (intent_json or {}).get("intent") or "unknown"
    need_clarify = bool((intent_json or {}).get("need_clarify"))
    sales_signal = bool((intent_json or {}).get("sales_signal"))
    slots = (intent_json or {}).get("slots") or {}
    has_phone = bool(str(slots.get("phone","") or "").strip())

    # support intents
    if intent in ("buy_payment", "agency_policy", "hard_business", "complaint"):
        return "support"

    if need_clarify:
        return "identify"

    # greeting / tiny message
    if turns == 0 and len(t.strip()) <= 12 and any(x in t for x in ["chào", "hi", "hello", "alo"]):
        return "identify"

    # explicit order keywords
    if any(k in t for k in ["đặt", "mua", "chốt", "lên đơn", "ship", "cod", "thanh toán", "giá bao nhiêu", "link"]):
        return "close"

    if sales_signal or has_phone:
        return "close"

    # if we retrieved offer
    if combos or products:
        return "offer"

    # otherwise we know topic but are still exploring
    if _detect_topic_key(user_text):
        return "suggest"

    return "identify"


def build_stage_ctas(meta: dict, topic_key: str, profile_mode: str, stage: str, sales_signal: bool, turns: int) -> list:
    """Stage-based contextual CTAs."""
    meta = meta or {}
    ctas = []

    topic_labels = {
        "da_day": ("Xem combo dạ dày", "Đau dạ dày / trào ngược dùng combo nào?"),
        "duong_huyet": ("Xem combo đường huyết", "Người bị tiểu đường dùng combo nào?"),
        "mo_mau": ("Xem combo mỡ máu", "Mỡ máu cao dùng combo nào?"),
        "xuong_khop": ("Xem combo xương khớp", "Đau xương khớp dùng sản phẩm/combo nào?"),
        "giac_ngu": ("Xem giải pháp giấc ngủ", "Mất ngủ/lo âu nên dùng sản phẩm nào?"),
    }

    def add_contacts():
        if meta.get("zalo"):
            ctas.append({"label": "Zalo 1-1", "action": "link", "url": str(meta.get("zalo"))})
        if meta.get("fanpage"):
            ctas.append({"label": "Fanpage", "action": "link", "url": str(meta.get("fanpage"))})

    # Stage rules:
    # identify: no CTA
    if stage == "identify":
        return []

    # suggest: ONLY show "Xem combo ..." for detected topic
    if stage == "suggest":
        if topic_key in topic_labels:
            label, payload = topic_labels[topic_key]
            ctas.append({"label": label, "action": "send", "payload": payload})
        return ctas

    # offer: show "Xem combo ..." + (optional) ask order, but NOT push hard if profile is CSKH_LIGHT
    if stage == "offer":
        if topic_key in topic_labels:
            label, payload = topic_labels[topic_key]
            ctas.append({"label": label, "action": "send", "payload": payload})
        if profile_mode == "SALES":
            # soft order
            if topic_key == "da_day":
                ctas.append({"label": "Đặt combo dạ dày", "action": "send", "payload": "Em muốn đặt combo dạ dày. Nhờ em chốt đơn giúp (COD) nhé."})
            else:
                ctas.append({"label": "Đặt nhanh", "action": "send", "payload": "Em muốn đặt hàng nhanh. Nhờ em chốt đơn giúp (COD) nhé."})
        add_contacts()
        return ctas

    # close: prioritize order + contact
    if stage == "close":
        if profile_mode == "SALES":
            if topic_key == "da_day":
                ctas.append({"label": "Chốt combo dạ dày (COD)", "action": "send", "payload": "Chốt giúp em combo dạ dày (COD). Em gửi SĐT + địa chỉ ngay."})
            else:
                ctas.append({"label": "Chốt đơn (COD)", "action": "send", "payload": "Chốt đơn giúp em (COD). Em gửi SĐT + địa chỉ ngay."})
        add_contacts()
        return ctas

    # support: contact only
    if stage == "support":
        add_contacts()
        return ctas

    # fallback
    return build_contextual_ctas(meta, topic_key, profile_mode, sales_signal, turns)
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
            # Ask as 1 message (natural)
            reply = "Dạ em hỏi nhanh 1–2 ý để tư vấn đúng hơn ạ:\n- " + "\n- ".join(qs)
            return jsonify({"reply": reply}), 200

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
        # topic/pronoun for contextual CTA
        topic_key = _detect_topic_key(user_text) or str(problem_key or "")
        pronoun = ctx.get("pronoun") or _detect_pronoun(user_text)
        ctx["pronoun"] = pronoun
        memory_store.set(session_id, ctx)

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

        memory_store.update(session_id, {
            "turns": turns + 1,
            "problem_key": problem_key or ctx.get("problem_key",""),
            "last_intent": intent,
            "tone": intent_json.get("tone","friendly"),
        })
        
    # ---------- stage-based CTA ----------
    topic_key2 = _detect_topic_key(user_text) or str(problem_key or ctx.get("problem_key") or "")
    stage = detect_stage(user_text=user_text, intent_json=intent_json, turns=turns, combos=combos, products=products)
    ctas = build_stage_ctas(store.meta, topic_key2, PROFILE_MODE, stage, bool(intent_json.get("sales_signal")), turns)

    return jsonify({
        "reply": reply,
        "meta": {
            "topic": topic_key2,
            "pronoun": ctx.get("pronoun", "anh/chị"),
            "stage": stage,
            "ctas": ctas
        }
    }), 200
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
    # build contextual CTAs
    topic_key2 = _detect_topic_key(user_text) or str(ctx.get("problem_key") or "")
    ctas = build_contextual_ctas(store.meta, topic_key2, PROFILE_MODE, bool(body.get("sales_signal") or False) or bool((locals().get("intent_json") or {}).get("sales_signal")), turns)
    return jsonify({"reply": reply, "meta": {"topic": topic_key2, "pronoun": ctx.get("pronoun","anh/chị"), "ctas": ctas}}), 200

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
