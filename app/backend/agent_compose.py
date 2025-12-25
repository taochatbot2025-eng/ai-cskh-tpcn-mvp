from __future__ import annotations
import os, json
from typing import Dict, Any, List, Optional
from openai import OpenAI

def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def compose_reply(
    meta: Dict[str, Any],
    profile: Dict[str, Any],
    user_text: str,
    intent_json: Dict[str, Any],
    combos: List[Dict[str, Any]],
    products: List[Dict[str, Any]],
    faqs: List[Dict[str, Any]],
    handoff: Optional[Dict[str, Any]],
    ctx: Dict[str, Any],
    lead_saved: Optional[Dict[str, Any]] = None
) -> str:
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    profile_mode = os.getenv("PROFILE_MODE", "SALES").upper()

    # lightweight "agent feel" rules
    sys = """Bạn là trợ lý AI CSKH cho doanh nghiệp TPCN. Viết tiếng Việt tự nhiên, thân thiện, linh hoạt như người thật.
RÀNG BUỘC BẮT BUỘC:
- Không chẩn đoán, không cam kết khỏi bệnh, không dùng từ 'chữa khỏi', 'đặc trị'. Có thể nói 'hỗ trợ', 'cải thiện'.
- Không bịa dữ liệu. Tên/giá/link/thành phần/cách dùng chỉ dùng từ dữ liệu được cung cấp.
- Nếu có risk_flags quan trọng (pregnant/child/severe_symptoms/drug_interaction/ask_cure_guarantee) thì ưu tiên khuyến nghị gặp CSKH/hotline, và trả lời thận trọng.
- Nếu handoff có dữ liệu hotline/fanpage/zalo thì hướng dẫn liên hệ rõ ràng.
- Tránh chào hỏi lặp lại. Nếu ctx.turns >= 1 thì vào thẳng giải pháp, chỉ mở câu ngắn gọn.

PHONG CÁCH:
- Trình bày gọn, dễ đọc: tiêu đề ngắn + gạch đầu dòng.
- Với COMBO: nêu combo, giá, link; liệt kê sản phẩm trong combo (tên, giá, lợi ích, cách dùng).
- Với SẢN PHẨM: nêu 2-4 sản phẩm phù hợp (tên, thành phần/điểm nổi bật, cách dùng, link).
- Với MUA HÀNG/THANH TOÁN: hướng dẫn theo policy/FAQ.
- Với SALES mode: nếu sales_signal=true thì chốt mềm: xin SĐT + tỉnh/thành để lên đơn nhanh, hoặc đưa link tự đặt.
"""

    payload = {
        "company": meta,
        "profile": profile,
        "profile_mode": profile_mode,
        "user_text": user_text,
        "intent_json": intent_json,
        "ctx": {k: ctx.get(k) for k in ["turns","problem_key","last_intent","tone"]},
        "combos": combos,
        "products": products,
        "faqs": faqs,
        "handoff": handoff,
        "lead_saved": lead_saved
    }

    try:
        resp = _client().responses.create(
            model=model,
            input=[
                {"role":"system","content":sys},
                {"role":"user","content":json.dumps(payload, ensure_ascii=False)}
            ]
        )
        return (resp.output_text or "").strip() or "Dạ em đã ghi nhận. Anh/chị cho em xin thêm 1 thông tin để hỗ trợ đúng hơn ạ 😊"
    except Exception:
        # safe fallback
        if handoff and (handoff.get("hotline") or handoff.get("fanpage") or handoff.get("zalo")):
            parts = []
            if handoff.get("hotline"): parts.append(f"Hotline: {handoff.get('hotline')}")
            if handoff.get("zalo"): parts.append(f"Zalo: {handoff.get('zalo')}")
            if handoff.get("fanpage"): parts.append(f"Fanpage: {handoff.get('fanpage')}")
            return "Dạ để hỗ trợ nhanh và chính xác hơn, anh/chị vui lòng liên hệ: " + " • ".join(parts)
        return "Dạ hệ thống đang bận một chút. Anh/chị cho em xin SĐT để bên em hỗ trợ nhanh qua hotline nhé ạ 😊"
