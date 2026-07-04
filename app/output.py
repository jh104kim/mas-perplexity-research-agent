from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9가-힣_-]+", "-", value).strip("-")
    return slug[:48] or "research"


def make_dated_output_dir(base_dir: str | Path, topic: str, now: datetime | None = None) -> Path:
    current = now or datetime.now()
    folder = f"{current:%Y%m%d-%H%M%S}-{slugify(topic)}"
    path = Path(base_dir) / folder
    path.mkdir(parents=True, exist_ok=False)
    return path

