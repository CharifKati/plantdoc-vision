"""
ip_blocklist.py
---------------
Automatically bans IPs that repeatedly hit the rate limit.
Rate limiting slows attackers down — this actually kicks them out.

How it works:
- Every time an IP hits the rate limit, their strike count goes up
- At 3 strikes they are banned for BAN_DURATION_MINUTES
- Bans expire automatically — no manual intervention needed
- All actions are logged via logger.py
"""

from datetime import datetime, timedelta
from collections import defaultdict
from .logger import log_blocklist

BAN_DURATION_MINUTES = 15
MAX_STRIKES          = 3

# In-memory store — resets on server restart (fine for a 48h MVP)
_strikes: dict = defaultdict(int)
_bans:    dict = {}


def record_strike(ip: str) -> bool:
    """
    Call this every time an IP hits the rate limit.
    Returns True if the IP just got banned as a result.
    """
    _strikes[ip] += 1
    if _strikes[ip] >= MAX_STRIKES:
        _ban(ip)
        return True
    log_blocklist(ip, f"strike {_strikes[ip]} of {MAX_STRIKES}")
    return False


def _ban(ip: str) -> None:
    """Internal — bans an IP for BAN_DURATION_MINUTES."""
    _bans[ip] = datetime.now() + timedelta(minutes=BAN_DURATION_MINUTES)
    log_blocklist(ip, f"BANNED for {BAN_DURATION_MINUTES} minutes (strikes: {_strikes[ip]})")


def is_banned(ip: str) -> bool:
    """
    Call this at the top of every request — before anything else.
    Automatically lifts expired bans.

    Usage:
        if is_banned(request.client.host):
            return JSONResponse(status_code=403, content={"error": "Access denied"})
    """
    if ip not in _bans:
        return False

    if datetime.now() > _bans[ip]:
        # Ban expired — clean up
        del _bans[ip]
        _strikes[ip] = 0
        log_blocklist(ip, "BAN EXPIRED — access restored")
        return False

    return True


def get_status(ip: str) -> dict:
    """Returns current status of an IP — useful for debugging."""
    banned    = is_banned(ip)
    ban_until = _bans.get(ip)
    return {
        "ip":        ip,
        "banned":    banned,
        "strikes":   _strikes[ip],
        "ban_until": ban_until.strftime("%H:%M:%S") if ban_until else None,
    }
