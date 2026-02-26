"""
stats.py
--------
In-memory counters for the security dashboard.
Call these functions from logger.py to track events automatically.
"""

from datetime import datetime
from collections import deque

# ── Counters ──────────────────────────────────────────────────────────────────
_stats = {
    "total_requests":  0,
    "allowed":         0,
    "blocked":         0,
    "rate_limited":    0,
    "bans_issued":     0,
    "started_at":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

# Live log feed — last 50 entries
_log_feed = deque(maxlen=50)


# ── Public API ────────────────────────────────────────────────────────────────

def record_allowed(ip: str) -> None:
    _stats["total_requests"] += 1
    _stats["allowed"] += 1
    _log_feed.appendleft({
        "time":   _now(),
        "level":  "ALLOWED",
        "ip":     ip,
        "reason": "",
    })


def record_blocked(ip: str, reason: str) -> None:
    _stats["total_requests"] += 1
    _stats["blocked"] += 1
    _log_feed.appendleft({
        "time":   _now(),
        "level":  "BLOCKED",
        "ip":     ip,
        "reason": reason,
    })


def record_rate_limited(ip: str) -> None:
    _stats["total_requests"] += 1
    _stats["rate_limited"] += 1
    _log_feed.appendleft({
        "time":   _now(),
        "level":  "RATELIMIT",
        "ip":     ip,
        "reason": "Rate limit exceeded",
    })


def record_ban(ip: str, minutes: int) -> None:
    _stats["bans_issued"] += 1
    _log_feed.appendleft({
        "time":   _now(),
        "level":  "BANNED",
        "ip":     ip,
        "reason": f"Banned for {minutes} minutes",
    })


def get_stats() -> dict:
    return dict(_stats)


def get_log_feed() -> list:
    return list(_log_feed)


def _now() -> str:
    return datetime.now().strftime("%H:%M:%S")
