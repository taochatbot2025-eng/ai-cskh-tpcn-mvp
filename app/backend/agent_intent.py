from __future__ import annotations
import os, json
from typing import Dict, Any
from openai import OpenAI

JSON_ERR_FALLBACK = {
  "intent": "unknown",
  "problem_key": "",
  "slots": {},
  "need_clarify": True,
  "clarify_questions": ["Anh/chị cho em biết mình đang cần hỗ trợ vấn đề gì ạ (ví dụ: dạ dày, tiểu đường, mỡ máu…)?"],
  "risk_flags": [],
  "sales_signal": False,
  "handoff": False,
  "tone": "friendly"
}

def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_intent(user_text: str, ctx: Dict[str, Any], meta: Dict[str, Any], profile_mode: str) -> Dict[str, Any]:
    model = os.getenv("OPENAI_MODEL_INTENT", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    sys = """Bạn là bộ phân tích ý định cho chatbot CSKH Thực phẩm chức năng (TPCN).
Trả về JSON THUẦN (không markdown, không giải thích).

Mục tiêu:
- Hiểu ý định người dùng, trích xuất 'problem_key' theo các khóa chuẩn (ví dụ: tieu_duong, da_day, trao_nguoc, mo_mau, gan, xuong_khop, mat_ngu, giam_can, tang_can...).
- Nếu thiếu thông tin quan trọng để tư vấn, đặt tối đa 2 câu hỏi làm rõ trong 'clarify_questions'.
- Phát hiện tín hiệu mua hàng (hỏi giá, COD, ship, mua thế nào, link...) => sales_signal=true.
- Nếu nội dung thuộc "kinh doanh/đại lý/hoa hồng" hoặc yêu cầu cam kết kết quả, hoặc khiếu nại phức tạp => handoff=true.
- Nếu người dùng yêu cầu chẩn đoán, cam kết khỏi bệnh, thay thuốc, hoặc có yếu tố rủi ro (mang thai/cho con bú/trẻ em/triệu chứng nặng/đang dùng thuốc kê đơn) => thêm vào risk_flags và ưu tiên handoff nếu cần.

Schema JSON:
{
  "intent": "combo" | "product" | "buy_payment" | "agency_policy" | "hard_business" | "complaint" | "unknown",
  "problem_key": "tieu_duong|da_day|trao_nguoc|mo_mau|...",
  "slots": {"age": "", "gender": "", "severity": "", "current_meds": "", "budget": "", "goal": "", "area": "", "name": "", "phone": ""},
  "need_clarify": true/false,
  "clarify_questions": ["...", "..."],
  "risk_flags": ["pregnant","child","severe_symptoms","drug_interaction","ask_cure_guarantee", ...],
  "sales_signal": true/false,
  "handoff": true/false,
  "tone": "friendly" | "concise" | "formal"
}

Quy tắc hội thoại:
- Nếu ctx đã có problem_key, tận dụng; không hỏi lại.
- Không tự bịa sản phẩm/giá/link.
"""

    user = {
        "user_text": user_text,
        "ctx": {k: ctx.get(k) for k in ["problem_key","last_intent","turns","tone"] if k in ctx},
        "known_problem_keys": meta.get("known_problem_keys", []),
        "profile_mode": profile_mode
    }

    try:
        resp = _client().responses.create(
            model=model,
            input=[
                {"role":"system","content":sys},
                {"role":"user","content":json.dumps(user, ensure_ascii=False)}
            ]
        )
        raw = (resp.output_text or "").strip()
        data = json.loads(raw)
        # normalize
        data.setdefault("slots", {})
        data.setdefault("clarify_questions", [])
        data.setdefault("risk_flags", [])
        data.setdefault("tone", "friendly")
        data["problem_key"] = str(data.get("problem_key") or "").strip()
        data["intent"] = str(data.get("intent") or "unknown").strip()
        data["need_clarify"] = bool(data.get("need_clarify"))

        # use ctx problem if not provided
        if not data["problem_key"] and ctx.get("problem_key"):
            data["problem_key"] = ctx.get("problem_key","")
            data["need_clarify"] = False

        # cap questions
        qs = [q.strip() for q in (data.get("clarify_questions") or []) if str(q).strip()]
        data["clarify_questions"] = qs[:2]
        if data["need_clarify"] and not data["clarify_questions"]:
            data["clarify_questions"] = JSON_ERR_FALLBACK["clarify_questions"]

        return data
    except Exception:
        # fallback
        fb = dict(JSON_ERR_FALLBACK)
        if ctx.get("problem_key"):
            fb["problem_key"] = ctx["problem_key"]
            fb["need_clarify"] = False
        return fb
