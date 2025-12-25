from __future__ import annotations
import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI

def _money(v):
    try:
        if v is None or v == "":
            return ""
        n = int(float(v))
        return f"{n:,}".replace(",", ".") + "đ"
    except Exception:
        return str(v)

def format_product(p: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "product_id": p.get("product_id"),
        "product_name": p.get("product_name"),
        "price": _money(p.get("sale_price") or p.get("price")),
        "link": p.get("product_link"),
        "ingredients": p.get("ingredients"),
        "benefits": p.get("benefits"),
        "usage": p.get("usage"),
        "duration_note": p.get("duration_note"),
        "contraindication": p.get("contraindication"),
        "tags": p.get("tags"),
        "qty": p.get("qty", "")
    }

def format_combo(c: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "combo_id": c.get("combo_id"),
        "combo_name": c.get("combo_name"),
        "target_problem": c.get("target_problem"),
        "price": _money(c.get("combo_price")),
        "compare_price": _money(c.get("compare_price")),
        "combo_link": c.get("combo_link"),
        "included_products": c.get("included_products"),
        "usage_guide": c.get("usage_guide"),
        "plan_7d": c.get("plan_7d"),
        "plan_14d": c.get("plan_14d"),
        "plan_30d": c.get("plan_30d"),
        "plan_60d": c.get("plan_60d"),
        "notes": c.get("notes")
    }

def generate_reply(
    profile: Dict[str, Any],
    meta: Dict[str, Any],
    intent: str,
    user_text: str,
    combos: List[Dict[str, Any]],
    products: List[Dict[str, Any]],
    faqs: List[Dict[str, Any]],
    handoff: Optional[Dict[str, Any]] = None
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    mode = os.getenv("PROFILE_MODE", "SALES").upper()
    cta = meta.get("default_cta_sales") if mode == "SALES" else meta.get("default_cta_soft")
    disclaimer = meta.get("disclaimer") or "Sản phẩm không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."

    sys = f"""Bạn là {profile.get('bot_role','nhân viên CSKH')}. 
Mục tiêu: trả lời tự nhiên, dễ hiểu, nhưng CHỈ dùng dữ liệu trong CONTEXT.
Quy tắc bắt buộc:
- Không chẩn đoán bệnh. Không hứa 'khỏi', 'điều trị'.
- Không tự bịa sản phẩm/giá/link/cách dùng. Thiếu dữ liệu -> nói rõ và đề nghị kết nối CSKH.
- Nếu CONTEXT có handoff => ưu tiên chuyển người thật, không giải thích dài.
- Luôn kèm cảnh báo (disclaimer) theo mức độ phù hợp, tránh lặp quá nhiều.
Giọng điệu: {profile.get('tone',{}).get('style','thân thiện')}.
"""

    context = {
        "intent": intent,
        "combos": [format_combo(c) for c in combos],
        "products": [format_product(p) for p in products],
        "faqs": faqs,
        "handoff": handoff,
        "cta": cta,
        "disclaimer": disclaimer,
        "channels": meta.get("support_channels", {})
    }

    payload = {
        "user_text": user_text,
        "context": context,
        "output_requirements": [
            "Nếu intent là tư vấn: trả theo bullet rõ ràng (Tên, Giá, Link, Lợi ích, Cách dùng).",
            "Nếu có combo: ưu tiên combo, rồi liệt kê từng sản phẩm trong combo.",
            "Kết thúc bằng CTA phù hợp, không ép.",
            "Giữ câu trả lời gọn (8–16 dòng)."
        ]
    }

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": sys},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}
        ]
    )
    return resp.output_text
