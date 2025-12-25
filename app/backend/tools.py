from __future__ import annotations
from typing import Dict, Any, List, Optional

from data_store import DataStore

def tool_get_combo(store: DataStore, problem_key: str, limit: int = 2) -> List[Dict[str, Any]]:
    return store.find_combos_by_problem(problem_key, limit=limit)

def tool_get_combo_products(store: DataStore, combo: Dict[str, Any]) -> List[Dict[str, Any]]:
    return store.expand_combo_products(combo)

def tool_search_products(store: DataStore, problem_key: str, limit: int = 4) -> List[Dict[str, Any]]:
    return store.find_products_by_problem(problem_key, limit=limit)

def tool_get_faq(store: DataStore, intent: str, limit: int = 3) -> List[Dict[str, Any]]:
    return store.faq_by_intent(intent, limit=limit)

def tool_best_routing(store: DataStore, user_text: str) -> Optional[Dict[str, Any]]:
    return store.best_routing(user_text)

def tool_save_lead(meta: Dict[str, Any], lead: Dict[str, Any]) -> Dict[str, Any]:
    # Demo: return payload; production: write to Sheets/CRM/Postgres
    # IMPORTANT: don't store sensitive health data; only contact + intent.
    out = {
        "ok": True,
        "to": meta.get("sales_receiver", "CSKH"),
        "lead": {
            "name": lead.get("name",""),
            "phone": lead.get("phone",""),
            "area": lead.get("area",""),
            "need": lead.get("need","")
        }
    }
    return out
