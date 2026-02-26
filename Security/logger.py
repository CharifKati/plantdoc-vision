"""
logger.py
---------
Logs every suspicious or blocked request to a file and the terminal.
Also feeds the live security dashboard via stats.py.
"""

import logging
from datetime import datetime
from . import stats as _stats_module

LOG_FILE = "security.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger("plantdoc.security")


def log_blocked(ip: str, reason: str) -> None:
    logger.warning(f"[{_now()}] BLOCKED   | IP: {ip:<18} | reason: {reason}")
    _stats_module.record_blocked(ip, reason)


def log_allowed(ip: str) -> None:
    logger.info(f"[{_now()}] ALLOWED   | IP: {ip:<18}")
    _stats_module.record_allowed(ip)


def log_rate_limit(ip: str) -> None:
    logger.warning(f"[{_now()}] RATELIMIT | IP: {ip:<18} | limit exceeded")
    _stats_module.record_rate_limited(ip)


def log_blocklist(ip: str, action: str) -> None:
    logger.warning(f"[{_now()}] BLOCKLIST | IP: {ip:<18} | action: {action}")
    if "BANNED" in action.upper():
        _stats_module.record_ban(ip, 15)


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
