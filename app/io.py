from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

import yaml

from app.state import ResearchState, get_output_dir


def artifact_path(state: ResearchState, filename: str) -> Path:
    return get_output_dir(state) / filename


def write_text_artifact(state: ResearchState, filename: str, content: str) -> Path:
    path = artifact_path(state, filename)
    path.write_text(content, encoding="utf-8")
    return path


def write_json_artifact(state: ResearchState, filename: str, data: Any) -> Path:
    path = artifact_path(state, filename)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_yaml_artifact(state: ResearchState, filename: str, data: Any) -> Path:
    path = artifact_path(state, filename)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def markdown_to_html(markdown: str, title: str = "Research Report") -> str:
    lines = markdown.splitlines()
    body: list[str] = []
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            body.append("</ul>")
            in_list = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            close_list()
            continue
        if stripped.startswith("# "):
            close_list()
            body.append(f"<h1>{escape(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            close_list()
            body.append(f"<h2>{escape(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            close_list()
            body.append(f"<h3>{escape(stripped[4:])}</h3>")
        elif stripped.startswith("- "):
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{escape(stripped[2:])}</li>")
        else:
            close_list()
            body.append(f"<p>{escape(stripped)}</p>")
    close_list()

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="ko">',
            "<head>",
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            f"  <title>{escape(title)}</title>",
            "  <style>body{font-family:Arial,sans-serif;line-height:1.6;max-width:880px;margin:40px auto;padding:0 20px;color:#1f2937}h1,h2,h3{color:#111827}code{background:#f3f4f6;padding:2px 4px;border-radius:4px}</style>",
            "</head>",
            "<body>",
            *body,
            "</body>",
            "</html>",
        ]
    )

