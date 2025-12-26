# app/backend/app.py
import os, re, time
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

# ---------- App ----------
app = Flask(__name__, static_folder="../frontend", static_url_path="")
# ensure Vietnamese chars in JSON
try:
    app.json.ensure_ascii = False  # Flask 2.3+
except Exception:
    pass

# ---------- ENV / Config ----------
PROFILE_MODE = (os.getenv("PROFILE_MODE","SALES") or "SALES").upper()  # SOFT | SALES
BOT_NAME = os.getenv("BOT_NAME","Trợ lý AI TPCN")
BOT_TAG = os.getenv("BOT_TAG","AI-CSKH-TPCN")
ZALO_URL = os.getenv("ZALO_OA_URL", os.getenv("ZALO_URL",""))
FANPAGE_URL = os.getenv("FANPAGE_URL","")
ORDER_URL = os.getenv("ORDER_URL","")
HOTLINE = os.getenv("HOTLINE","")

# Optional OpenAI (works if key present)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","").strip()
try:
    from openai import OpenAI  # type: ignore
    _openai_ok = bool(OPENAI_API_KEY)
    _client = OpenAI(api_key=OPENAI_API_KEY) if _openai_ok else None
except Exception:
    _openai_ok = False
    _client = None

# ---------- Minimal Catalog (demo) ----------
# Replace links via ENV if you want per-combo landing URLs
CATALOG = {
  "da_day": {
    "label":"Dạ dày",
    "combo_name":"Combo Hỗ Trợ Dạ Dày",
    "combo_price":"1.100.000 VNĐ",
    "combo_compare":"1.130.000 VNĐ",
    "combo_link": os.getenv("COMBO_DA_DAY_URL",""),
    "items":[
      {"name":"Viên hỗ trợ dạ dày", "price":"650.000 VNĐ", "benefit":"Hỗ trợ giảm cảm giác nóng rát, bảo vệ niêm mạc.", "usage":"Uống 2 viên/lần, ngày 2 lần trước ăn."},
      {"name":"Hỗ trợ gan – giải độc", "price":"480.000 VNĐ", "benefit":"Hỗ trợ chức năng gan, giảm nóng trong.", "usage":"Uống 2 viên/ngày sau ăn."},
    ],
    "plan":[("7 ngày","Giảm cảm giác cồn cào"),("14 ngày","Ăn uống dễ chịu hơn"),("30 ngày","Hỗ trợ bảo vệ niêm mạc dạ dày"),("60 ngày","Duy trì nếu ăn uống điều độ")],
    "note":"Tránh rượu bia, đồ cay nóng. Nếu đau dữ dội/nôn ra máu/đi ngoài phân đen nên đi khám."
  },
  "xuong_khop": {
    "label":"Xương khớp",
    "combo_name":"Combo Hỗ Trợ Xương Khớp",
    "combo_price":"1.190.000 VNĐ",
    "combo_compare":"",
    "combo_link": os.getenv("COMBO_XUONG_KHOP_URL",""),
    "items":[
      {"name":"TPBVSK Xương Khớp A", "price":"690.000 VNĐ", "benefit":"Hỗ trợ giảm khó chịu, hỗ trợ vận động.", "usage":"Uống 2 viên/ngày sau ăn."},
      {"name":"TPBVSK Dẻo Khớp B", "price":"550.000 VNĐ", "benefit":"Hỗ trợ bôi trơn khớp, duy trì sụn khớp.", "usage":"Uống 1 viên/ngày sau ăn."},
    ],
    "plan":[("7 ngày","Giảm ê mỏi sau vận động"),("14 ngày","Đỡ cứng khớp buổi sáng"),("30 ngày","Hỗ trợ vận động linh hoạt hơn")],
    "note":"Nếu sưng nóng đỏ khớp/đau tăng nhanh nên đi khám để loại trừ viêm cấp."
  },
  "duong_huyet": {"label":"Đường huyết","combo_name":"Combo Hỗ Trợ Đường Huyết","combo_price":"1.250.000 VNĐ","combo_compare":"","combo_link":os.getenv("COMBO_DUONG_HUYET_URL",""),"items":[],"plan":[],"note":"Không thay thế thuốc điều trị. Cần theo dõi đường huyết đều."},
  "mo_mau": {"label":"Mỡ máu","combo_name":"Combo Hỗ Trợ Mỡ Máu","combo_price":"1.180.000 VNĐ","combo_compare":"","combo_link":os.getenv("COMBO_MO_MAU_URL",""),"items":[],"plan":[],"note":"Kết hợp ăn nhạt, giảm mỡ động vật."},
  "gan": {"label":"Gan","combo_name":"Combo Hỗ Trợ Gan","combo_price":"990.000 VNĐ","combo_compare":"","combo_link":os.getenv("COMBO_GAN_URL",""),"items":[],"plan":[],"note":"Hạn chế bia rượu, ngủ đủ."},
  "giac_ngu": {"label":"Giấc ngủ","combo_name":"Combo Hỗ Trợ Giấc Ngủ","combo_price":"890.000 VNĐ","combo_compare":"","combo_link":os.getenv("COMBO_GIAC_NGU_URL",""),"items":[],"plan":[],"note":"Giữ lịch ngủ đều, giảm caffeine sau 14h."},
}

TOPIC_PATTERNS = [
  ("da_day", r"(dạ dày|trào ngược|đầy hơi|ợ chua|đau bụng|viêm dạ dày)"),
  ("xuong_khop", r"(xương khớp|khớp|đau khớp|thoái hóa|cứng khớp|đau gối|đau vai|đau lưng)"),
  ("duong_huyet", r"(tiểu đường|đường huyết|đái tháo đường|hba1c)"),
  ("mo_mau", r"(mỡ máu|cholesterol|triglycerid)"),
  ("gan", r"(gan|men gan|nóng trong|giải độc)"),
  ("giac_ngu", r"(mất ngủ|khó ngủ|ngủ không sâu|stress|lo âu)"),
]
BUY_PAT = r"(mua|đặt|chốt|ship|giao|cod|thanh toán|giá|ưu đãi|link|đơn hàng)"
OK_PAT = r"^(ok|oke|được|chốt|mua|lấy|đặt|gửi link|gửi đơn|tư vấn 1-1)$"

# ---------- Simple memory (per visitor via cookie id) ----------
_MEM = {}

def _sid():
    sid = request.cookies.get("sid")
    if sid:
        return sid
    # fallback: simple fingerprint
    ip = request.headers.get("x-forwarded-for", request.remote_addr) or "0"
    ua = request.headers.get("user-agent","")[:40]
    return f"{hash(ip+ua)%10**10}"

def _mem():
    sid=_sid()
    if sid not in _MEM:
        _MEM[sid]={"turns":0,"stage":"identify","topic":"","asked":0,"last_offer_topic":"","last_ctas":[]}
    return _MEM[sid]

def detect_topic(text: str):
    t=(text or "").lower()
    for k,pat in TOPIC_PATTERNS:
        if re.search(pat, t, re.I):
            return k
    return ""

def detect_stage(text: str, mem: dict):
    t=(text or "").lower()
    topic = mem.get("topic","")
    stage = mem.get("stage","identify")
    buy = bool(re.search(BUY_PAT, t, re.I))
    ok = bool(re.search(OK_PAT, t.strip(), re.I))
    # Stage jump signals
    if buy:
        return "close"
    if stage in ("offer","close") and ok:
        return "close"
    if topic and stage == "identify":
        return "suggest"
    if stage == "suggest" and mem.get("asked",0) >= 1:
        return "offer"
    return stage

def build_ctas(topic_key: str, stage: str):
    ctas=[]
    # topic CTA
    if topic_key and stage in ("suggest","offer"):
        label = f"Xem combo {CATALOG[topic_key]['label'].lower()}" if topic_key in CATALOG else "Xem combo"
        ctas.append({"label": label, "action":"send", "payload": f"Cho em xem combo {CATALOG[topic_key]['label'].lower()} nhé"})
    # order/contact
    def add_contacts():
        if ZALO_URL: ctas.append({"label":"Zalo 1-1","action":"link","url":ZALO_URL})
        if FANPAGE_URL: ctas.append({"label":"Fanpage","action":"link","url":FANPAGE_URL})
        if HOTLINE: ctas.append({"label":"Gọi hotline","action":"link","url": f"tel:{HOTLINE}"})
    if PROFILE_MODE=="SALES":
        if stage in ("offer","close"):
            url = ORDER_URL or ZALO_URL or FANPAGE_URL
            if url:
                ctas.insert(0, {"label":"Đặt nhanh","action":"link","url":url})
        if stage in ("offer","close","support"):
            add_contacts()
    else:
        # SOFT: no order CTA
        if stage in ("offer","support"):
            add_contacts()
    return ctas

def soft_prefix():
    return "" if PROFILE_MODE=="SALES" else "Dạ "

def reply_identify():
    return f"{soft_prefix()}chào anh/chị 😊 Em là **{BOT_NAME}** (TPCN thiên nhiên). Anh/chị đang quan tâm nhóm nào ạ: dạ dày/đường huyết/mỡ máu/gan/xương khớp/giấc ngủ?"

def reply_suggest(topic_key: str, mem: dict):
    label = CATALOG.get(topic_key,{}).get("label","vấn đề này")
    # ask 1 focused question
    q1 = {
      "da_day":"Anh/chị thường khó chịu kiểu nào: **ợ chua/nóng rát/đầy hơi/đau âm ỉ** ạ?",
      "xuong_khop":"Anh/chị đang khó chịu chủ yếu ở **gối/lưng/vai/cổ tay** hay **cứng khớp buổi sáng** ạ?",
      "duong_huyet":"Anh/chị có đang theo dõi **đường huyết** gần đây không ạ?",
      "mo_mau":"Anh/chị có kết quả **mỡ máu** gần đây (cholesterol/triglycerid) không ạ?",
      "gan":"Anh/chị đang quan tâm **men gan/nóng trong/giải độc** hay **gan nhiễm mỡ** ạ?",
      "giac_ngu":"Anh/chị khó ngủ do **stress/đầu óc suy nghĩ** hay **thức giấc giữa đêm** ạ?",
    }.get(topic_key, "Anh/chị cho em biết triệu chứng cụ thể nhất đang gặp ạ?")
    mem["asked"]=mem.get("asked",0)+1
    return f"Về **{label}**, em hỏi nhanh 1 câu để tư vấn đúng hơn nhé: {q1}"

def render_combo(topic_key: str):
    c = CATALOG.get(topic_key)
    if not c:
        return "Dạ em chưa có combo phù hợp trong hệ thống. Anh/chị cho em biết thêm nhu cầu ạ?"
    lines=[]
    lines.append(f"**{c['combo_name']}**")
    if c.get("combo_compare"):
        lines.append(f"- **Giá:** {c['combo_price']} (giá gốc: {c['combo_compare']})")
    else:
        lines.append(f"- **Giá:** {c['combo_price']}")
    if c.get("items"):
        lines.append("- **Gồm:**")
        for it in c["items"]:
            lines.append(f"  - **{it['name']}** ({it['price']})")
            if it.get("benefit"): lines.append(f"    - Lợi ích: {it['benefit']}")
            if it.get("usage"): lines.append(f"    - Cách dùng: {it['usage']}")
    if c.get("plan"):
        lines.append("- **Kế hoạch tham khảo:**")
        for d,txt in c["plan"]:
            lines.append(f"  - {d}: {txt}")
    if c.get("note"):
        lines.append(f"⚠️ **Lưu ý:** {c['note']}")
    if c.get("combo_link"):
        lines.append(f"👉 Xem chi tiết: [{c['combo_name']}]({c['combo_link']})")
    return "\n".join(lines)

def reply_offer(topic_key: str):
    if PROFILE_MODE=="SALES":
        tail="\n\nAnh/chị muốn **em gửi link đặt hàng + ưu đãi hiện tại** không ạ?"
    else:
        tail="\n\nNếu anh/chị muốn, em gửi **link xem chi tiết** và hướng dẫn dùng phù hợp ạ."
    return render_combo(topic_key) + tail

def reply_close(topic_key: str):
    if PROFILE_MODE=="SALES":
        url = ORDER_URL or CATALOG.get(topic_key,{}).get("combo_link") or ZALO_URL or FANPAGE_URL
        if url:
            return f"Dạ được ạ ✅ Em gửi anh/chị link **đặt nhanh** ở đây: {url}\n\nAnh/chị cho em xin *tỉnh/thành + SĐT* để em hỗ trợ chốt đơn/ship nhanh nhé."
        return "Dạ được ạ ✅ Anh/chị cho em xin *tỉnh/thành + SĐT* để em hỗ trợ chốt đơn nhé."
    else:
        return "Dạ em sẵn sàng hỗ trợ 😊 Anh/chị cho em biết thêm nhu cầu/độ tuổi/đang dùng thuốc gì (nếu có) để em hướng dẫn an toàn hơn ạ."

def maybe_llm(user_text: str, mem: dict, topic_key: str, stage: str):
    """Optional: use OpenAI to paraphrase into more natural Vietnamese while respecting stage rules."""
    if not _openai_ok or not _client:
        return None
    # Keep it short and sales-safe
    sys = f"""Bạn là trợ lý CSKH TPCN tại Việt Nam.
PROFILE_MODE={PROFILE_MODE}. STAGE={stage}. TOPIC={topic_key or 'none'}.
Quy tắc:
- Không chào lại nếu đã có ít nhất 1 lượt.
- Ưu tiên hỏi tối đa 1 câu làm rõ ở STAGE=suggest; nếu đủ thì sang offer.
- Ở offer: đưa đúng 1 phương án chính, trình bày gọn (không lan man), không hứa khỏi bệnh.
- Ở close: xin thông tin chốt đơn; không ép.
- Văn phong thân thiện, chuyên nghiệp, ngắn gọn.
"""
    draft = {
      "identify": reply_identify(),
      "suggest": reply_suggest(topic_key, {"asked":0}),
      "offer": reply_offer(topic_key),
      "close": reply_close(topic_key),
      "support": "Dạ anh/chị cần hỗ trợ mua hàng/ship/COD hay chính sách ạ?"
    }.get(stage, reply_identify())
    try:
        r=_client.responses.create(
            model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
            input=[{"role":"system","content":sys},
                   {"role":"user","content":f"Người dùng: {user_text}\n\nHãy viết lại câu trả lời sau cho tự nhiên hơn (giữ nguyên ý):\n---\n{draft}\n---"}],
            temperature=0.5,
        )
        out=r.output_text.strip()
        return out or None
    except Exception:
        return None

# ---------- Routes ----------
@app.get("/")
def root():
    return send_from_directory(app.static_folder, "index.html")

@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "profile_mode": PROFILE_MODE,
        "openai_enabled": _openai_ok,
        "ts": datetime.utcnow().isoformat()+"Z"
    })

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    msg = (data.get("message") or "").strip()
    if not msg:
        return jsonify({"reply":"Dạ anh/chị gửi giúp em nội dung cần tư vấn nhé 😊", "meta":{"stage":"identify","topic":"","ctas":[]}})

    mem=_mem()
    mem["turns"]=mem.get("turns",0)+1

    # topic detect (persist once found unless user switches)
    new_topic = detect_topic(msg)
    if new_topic:
        mem["topic"]=new_topic

    # stage engine
    mem["stage"]=detect_stage(msg, mem)
    stage=mem["stage"]
    topic=mem.get("topic","")

    # Build reply deterministically
    if mem["turns"] <= 1:
        reply = reply_identify()
        stage="identify"
        topic=topic or ""
        mem["stage"]=stage
    else:
        if stage == "identify":
            reply = reply_identify()
        elif stage == "suggest":
            reply = reply_suggest(topic, mem)
        elif stage == "offer":
            reply = reply_offer(topic)
        elif stage == "close":
            reply = reply_close(topic)
        else:
            reply = "Dạ anh/chị cho em biết thêm nhu cầu để em hỗ trợ tốt hơn ạ 😊"

    # Optional: polish by LLM
    polished = maybe_llm(msg, mem, topic, stage)
    if polished:
        reply = polished

    ctas = build_ctas(topic, stage)
    meta = {
        "stage": stage,
        "topic": topic,
        "profile_mode": PROFILE_MODE,
        "ctas": ctas,
        "zalo": ZALO_URL,
        "fanpage": FANPAGE_URL,
        "order": ORDER_URL,
    }

    resp = jsonify({"reply": reply, "meta": meta})
    # set sid cookie if missing
    if not request.cookies.get("sid"):
        resp.set_cookie("sid", _sid(), max_age=60*60*24*30, samesite="Lax")
    return resp

# Static files (css/js/img)
@app.get("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    # Render will use gunicorn; local run:
    app.run(host="0.0.0.0", port=int(os.getenv("PORT","10000")), debug=False)
