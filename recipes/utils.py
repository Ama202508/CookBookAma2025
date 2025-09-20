from datetime import datetime

_ALLOWED_FORMATS = [
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%d.%m.%Y %H:%M",
    "%d.%m.%Y",
    "%Y/%m/%d %H:%M",
]

def normalize_date_string(s: str) -> str:
    s = (s or "").strip()
    for fmt in _ALLOWED_FORMATS:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            continue
    raise ValueError("Format dată invalid. Ex: 2025-09-11 14:30 sau 11.09.2025 14:30")
