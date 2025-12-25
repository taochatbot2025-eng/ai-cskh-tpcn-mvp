from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
import pandas as pd

@dataclass
class DataStore:
    products: pd.DataFrame
    combos: pd.DataFrame
    faq: pd.DataFrame
    routing: pd.DataFrame
    meta: dict
    alias_tags: dict

    @staticmethod
    def load(data_dir: str) -> "DataStore":
        d = Path(data_dir).resolve()
        products = pd.read_csv(d / "01_PRODUCTS.csv")
        combos = pd.read_csv(d / "02_COMBOS.csv")
        faq = pd.read_csv(d / "03_FAQ.csv")
        routing = pd.read_csv(d / "04_ROUTING.csv")
        meta = json.loads((d / "05_META.json").read_text(encoding="utf-8"))

        alias_path = d / "10_ALIAS_TAGS.json"
        alias_tags = json.loads(alias_path.read_text(encoding="utf-8")) if alias_path.exists() else {}
        # normalize missing columns
        for col in ["sale_price","contraindication","duration_note","tags","status","ingredients","benefits","usage","problems","product_link"]:
            if col not in products.columns:
                products[col] = ""
        for col in ["status","combo_link","notes","plan_7d","plan_14d","plan_30d","plan_60d","usage_guide","compare_price"]:
            if col not in combos.columns:
                combos[col] = ""
        for col in ["priority","status"]:
            if col not in faq.columns:
                faq[col] = 1 if col=="priority" else "active"
        for col in ["status","working_hours","fanpage","zalo","trigger_intents"]:
            if col not in routing.columns:
                routing[col] = ""
        return DataStore(products, combos, faq, routing, meta, alias_tags)

    def find_products_by_problem(self, problem_key: str, limit: int = 3):
        df = self.products.copy()
        df = df[df["status"].fillna("active").str.lower().eq("active")]
        # match in problems column
        mask = df["problems"].fillna("").str.lower().str.contains(problem_key.lower(), na=False)
        cand = df[mask]
        if cand.empty:
            # try tags
            mask2 = df["tags"].fillna("").str.lower().str.contains(problem_key.lower(), na=False)
            cand = df[mask2]
        return cand.head(limit).to_dict(orient="records")

    def find_combos_by_problem(self, problem_key: str, limit: int = 2):
        df = self.combos.copy()
        df = df[df["status"].fillna("active").str.lower().eq("active")]
        cand = df[df["target_problem"].fillna("").str.lower().eq(problem_key.lower())]
        return cand.head(limit).to_dict(orient="records")

    def expand_combo_products(self, combo: dict):
        inc = str(combo.get("included_products",""))
        parts = [p.strip() for p in inc.split("|") if p.strip()]
        items = []
        for p in parts:
            # format: SP001 x1
            tok = p.split()
            pid = tok[0].strip()
            row = self.products[self.products["product_id"].astype(str) == pid]
            if not row.empty:
                r = row.iloc[0].to_dict()
                r["qty"] = " ".join(tok[1:]).strip() if len(tok)>1 else ""
                items.append(r)
        return items

    def faq_by_intent(self, intent: str, limit: int = 3):
        df = self.faq.copy()
        df = df[df["status"].fillna("active").str.lower().eq("active")]
        df = df[df["intent"].astype(str).str.lower().eq(intent.lower())]
        df = df.sort_values(by="priority", ascending=True) if "priority" in df.columns else df
        return df.head(limit).to_dict(orient="records")

    def best_routing(self, user_text: str):
        t = user_text.lower()
        df = self.routing.copy()
        df = df[df["status"].fillna("active").astype(str).str.lower().eq("active")]
        best = None
        best_hits = 0
        for _, row in df.iterrows():
            kws = str(row.get("trigger_keywords",""))
            kw_list = [k.strip().lower() for k in kws.split(";") if k.strip()]
            hits = sum(1 for k in kw_list if k and k in t)
            if hits > best_hits:
                best_hits = hits
                best = row.to_dict()
        return best if best_hits>0 else None
