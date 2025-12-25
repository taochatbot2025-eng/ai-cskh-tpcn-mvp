from __future__ import annotations
import time
from typing import Dict, Any, Optional

# Simple in-memory session store (good for demo).
# For production: swap to Redis/Postgres.
_SESS: Dict[str, Dict[str, Any]] = {}

DEFAULT_TTL_SEC = 60 * 60 * 6  # 6 hours

def _now() -> float:
    return time.time()

def get(session_id: str) -> Dict[str, Any]:
    if not session_id:
        session_id = "anon"
    s = _SESS.get(session_id) or {}
    exp = s.get("_exp")
    if exp and exp < _now():
        _SESS.pop(session_id, None)
        return {}
    return s

def set(session_id: str, data: Dict[str, Any], ttl_sec: int = DEFAULT_TTL_SEC) -> None:
    if not session_id:
        session_id = "anon"
    data = dict(data or {})
    data["_exp"] = _now() + max(60, int(ttl_sec or DEFAULT_TTL_SEC))
    _SESS[session_id] = data

def update(session_id: str, patch: Dict[str, Any], ttl_sec: int = DEFAULT_TTL_SEC) -> Dict[str, Any]:
    cur = get(session_id)
    cur.update(patch or {})
    set(session_id, cur, ttl_sec=ttl_sec)
    return cur

def cleanup() -> None:
    t = _now()
    for k in list(_SESS.keys()):
        exp = _SESS.get(k, {}).get("_exp")
        if exp and exp < t:
            _SESS.pop(k, None)
