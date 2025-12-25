from __future__ import annotations
import json
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

def _read_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [{k: (v if v is not None else "") for k, v in r.items()} for r in reader]

def _lower(s: Any) -> str:
    return str(s or "").strip().lower()

@dataclass
class DataStore:
    products: List[Dict[str, Any]]
    combos: List[Dict[str, Any]]
    faq: List[Dict[str, Any]]
    routing: List[Dict[str, Any]]
    meta: Dict[str, Any]
    alias_tags: Dict[str, Any]

    @staticmethod
    def load(data_dir: str) -> "DataStore":
        d = Path(data_dir).resolve()
        products = _read_csv(d / "01_PRODUCTS.csv")
        combos = _read_csv(d / "02_COMBOS.csv")
        faq = _read_csv(d / "03_FAQ.csv")
        routing = _read_csv(d / "04_ROUTING.csv")
        meta = json.loads((d / "05_META.json").read_text(encoding="utf-8"))

        alias_path = d / "10_ALIAS_TAGS.json"
        alias_tags = json.loads(alias_path.read_text(encoding="utf-8")) if alias_path.exists() else {}

        def ensure(rows, cols):
            for r in rows:
                for c in cols:
                    if c not in r:
                        r[c] = ""
        ensure(products, ["sale_price","price","contraindication","duration_note","tags","status","ingredients","benefits","usage","problems","product_link","product_id","product_name"])
        ensure(combos, ["status","combo_link","notes","plan_7d","plan_14d","plan_30d","plan_60d","usage_guide","compare_price","combo_price","included_products","target_problem","combo_id","combo_name"])
        ensure(faq, ["priority","status","intent","question","answer"])
        ensure(routing, ["status","working_hours","fanpage","zalo","trigger_intents","trigger_keywords","response_message","hotline"])

        return DataStore(products, combos, faq, routing, meta, alias_tags)

    def find_products_by_problem(self, problem_key: str, limit: int = 3) -> List[Dict[str, Any]]:
        pk = _lower(problem_key)
        out: List[Dict[str, Any]] = []
        for p in self.products:
            if _lower(p.get("status","active")) != "active":
                continue
            problems = _lower(p.get("problems",""))
            tags = _lower(p.get("tags",""))
            if pk and (pk in problems or pk in tags):
                out.append(p)
            if len(out) >= limit:
                break
        return out

    def find_combos_by_problem(self, problem_key: str, limit: int = 2) -> List[Dict[str, Any]]:
        pk = _lower(problem_key)
        out: List[Dict[str, Any]] = []
        for c in self.combos:
            if _lower(c.get("status","active")) != "active":
                continue
            if _lower(c.get("target_problem","")) == pk:
                out.append(c)
            if len(out) >= limit:
                break
        return out

    def expand_combo_products(self, combo: Dict[str, Any]) -> List[Dict[str, Any]]:
        inc = str(combo.get("included_products","") or "")
        parts = [p.strip() for p in inc.split("|") if p.strip()]
        items: List[Dict[str, Any]] = []
        idx = {str(p.get("product_id","")): p for p in self.products}
        for part in parts:
            tok = part.split()
            pid = tok[0].strip()
            row = idx.get(pid)
            if row:
                r = dict(row)
                r["qty"] = " ".join(tok[1:]).strip() if len(tok) > 1 else ""
                items.append(r)
        return items

    def faq_by_intent(self, intent: str, limit: int = 3) -> List[Dict[str, Any]]:
        it = _lower(intent)
        rows = [r for r in self.faq if _lower(r.get("status","active")) == "active" and _lower(r.get("intent","")) == it]
        def pr(x):
            try:
                return int(float(x.get("priority", 999) or 999))
            except Exception:
                return 999
        rows.sort(key=pr)
        return rows[:limit]

    def best_routing(self, user_text: str) -> Optional[Dict[str, Any]]:
        t = _lower(user_text)
        best = None
        best_hits = 0
        for row in self.routing:
            if _lower(row.get("status","active")) != "active":
                continue
            kws = str(row.get("trigger_keywords","") or "")
            kw_list = [k.strip().lower() for k in kws.split(";") if k.strip()]
            hits = sum(1 for k in kw_list if k in t)
            if hits > best_hits:
                best_hits = hits
                best = row
        return best if best_hits > 0 else None
