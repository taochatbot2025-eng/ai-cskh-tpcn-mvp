from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

@dataclass
class Router:
    cfg: Dict[str, Any]
    alias_tags: Dict[str, Any]

    @staticmethod
    def load(path: str, alias_tags: Dict[str, Any]) -> "Router":
        cfg = json.loads(Path(path).read_text(encoding="utf-8"))
        return Router(cfg, alias_tags or {})

    def _extract_problem(self, text: str) -> Optional[str]:
        t = text.lower()
        # 1) alias map if present
        amap = (self.cfg.get("entity_extractors", {}) or {}).get("problem", {}).get("map", {}) or {}
        if amap:
            for key, aliases in amap.items():
                for a in aliases:
                    if a.lower() in t:
                        return key
        # 2) alias_tags file
        p_alias = (self.alias_tags.get("problem_aliases") or {})
        for key, aliases in p_alias.items():
            for a in aliases:
                if a.lower() in t:
                    # Return key in router map style if possible
                    return key
        return None

    def is_safety_trigger(self, text: str) -> bool:
        t = text.lower()
        for w in (self.alias_tags.get("safety_triggers") or []):
            if str(w).lower() in t:
                return True
        return False

    def classify(self, text: str) -> Tuple[str, Optional[str]]:
        # Keyword first
        t = text.lower()
        if self.is_safety_trigger(text):
            # escalate later via handoff in flow
            return ("yeu_cau_cam_ket_ket_qua", self._extract_problem(text))

        intents = self.cfg.get("intents", [])
        best = ("ngoai_pham_vi", 0)
        for it in intents:
            score = 0
            for kw in it.get("keywords", []):
                if kw and kw.lower() in t:
                    score += 1
            if score > best[1] or (score == best[1] and it.get("priority", 0) > 0):
                best = (it.get("name", "ngoai_pham_vi"), score)
        return (best[0], self._extract_problem(text))
