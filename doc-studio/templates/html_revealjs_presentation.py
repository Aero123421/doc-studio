#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reveal.js (HTML) プレゼンテーションテンプレート
- CDN読み込みで手軽に実行
- ダーク基調 + アクセント配色
- 用途: 共有用HTMLスライド/軽量デモ
"""

import argparse
import datetime as _dt
import html as _html
import json
from pathlib import Path


DEFAULT_DATA = {
    "title": "Reveal.js Presentation",
    "subtitle": "Enterprise 2026",
    "company": "Enterprise Inc.",
    "date": _dt.date.today().strftime("%B %Y"),
    "theme": "black",
    "slides": [
        {"type": "title", "title": "Strategy Update", "subtitle": "2026 Roadmap"},
        {
            "type": "bullets",
            "title": "Agenda",
            "bullets": [
                "Executive summary",
                "KPIs & highlights",
                "Roadmap",
                "Risks & next steps",
            ],
        },
        {
            "type": "two_column",
            "title": "Current State",
            "left_title": "Strengths",
            "left_bullets": ["Delivery speed", "Customer trust", "Platform reliability"],
            "right_title": "Challenges",
            "right_bullets": ["Legacy components", "Data silos", "Cost optimization"],
        },
        {
            "type": "bullets",
            "title": "Next Steps",
            "bullets": ["Finalize plan", "Kickoff execution", "Measure weekly"],
        },
        {"type": "thanks", "title": "Thank You", "subtitle": "Questions & Discussion"},
    ],
}


def _load_data(args: argparse.Namespace) -> dict:
    if args.data and args.data_file:
        raise SystemExit("Use either --data or --data-file (not both)")

    if args.data_file:
        p = Path(args.data_file)
        return json.loads(p.read_text(encoding="utf-8"))

    if args.data:
        return json.loads(args.data)

    return {}


def _e(s: object) -> str:
    return _html.escape("" if s is None else str(s))


def _render_slide(slide: dict) -> str:
    slide_type = slide.get("type", "bullets")

    if slide_type == "title":
        return f"""
        <section class="title-slide">
          <h1>{_e(slide.get("title"))}</h1>
          <p class="subtitle">{_e(slide.get("subtitle"))}</p>
        </section>
        """

    if slide_type == "two_column":
        left_items = "\n".join(f"<li>{_e(x)}</li>" for x in slide.get("left_bullets", []))
        right_items = "\n".join(f"<li>{_e(x)}</li>" for x in slide.get("right_bullets", []))
        return f"""
        <section class="content-slide">
          <h2>{_e(slide.get("title"))}</h2>
          <div class="two-column">
            <div class="col">
              <h3>{_e(slide.get("left_title"))}</h3>
              <ul>{left_items}</ul>
            </div>
            <div class="col">
              <h3>{_e(slide.get("right_title"))}</h3>
              <ul>{right_items}</ul>
            </div>
          </div>
        </section>
        """

    if slide_type == "thanks":
        return f"""
        <section class="title-slide">
          <h1>{_e(slide.get("title", "Thank You"))}</h1>
          <p class="subtitle">{_e(slide.get("subtitle", ""))}</p>
        </section>
        """

    # default: bullets
    items = "\n".join(f"<li>{_e(x)}</li>" for x in slide.get("bullets", []))
    return f"""
    <section class="content-slide">
      <h2>{_e(slide.get("title"))}</h2>
      <ul>{items}</ul>
    </section>
    """


def generate_html(output_path: str, data: dict):
    merged = {**DEFAULT_DATA, **(data or {})}
    slides = merged.get("slides") or DEFAULT_DATA["slides"]
    theme = _e(merged.get("theme", "black"))

    sections = "\n".join(_render_slide(s) for s in slides)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_e(merged.get("title"))} - {_e(merged.get("subtitle"))}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reset.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/{theme}.css">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700&family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #1a365d;
      --secondary: #2c5282;
      --accent: #c9a227;
      --dark: #0d1117;
    }}
    .reveal {{ font-family: 'Noto Sans JP', 'Inter', sans-serif; }}
    .reveal h1, .reveal h2, .reveal h3 {{
      font-family: 'Inter', 'Noto Sans JP', sans-serif;
      text-transform: none;
      letter-spacing: -0.02em;
    }}
    .title-slide {{
      background: linear-gradient(135deg, var(--dark) 0%, var(--primary) 100%);
    }}
    .title-slide .subtitle {{
      color: rgba(255,255,255,0.85);
      margin-top: 1.5rem;
      font-size: 0.9em;
    }}
    .content-slide {{
      background: linear-gradient(180deg, var(--dark) 0%, #1a1f2e 100%);
    }}
    .content-slide h2 {{ color: var(--accent); }}
    .content-slide ul {{ font-size: 0.9em; line-height: 1.6; }}
    .two-column {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
      text-align: left;
      margin-top: 1rem;
    }}
    .two-column h3 {{ color: #00d4aa; }}
    .two-column .col {{ background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 12px; }}
    .slide-footer {{
      position: absolute;
      bottom: 20px;
      left: 30px;
      right: 30px;
      display: flex;
      justify-content: space-between;
      font-size: 0.5em;
      color: rgba(255,255,255,0.55);
    }}
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      {sections}
    </div>
  </div>

  <div class="slide-footer">
    <span>{_e(merged.get("company"))}</span>
    <span>{_e(merged.get("date"))}</span>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>
  <script>
    Reveal.initialize({{
      hash: true,
      slideNumber: 'c/t',
      transition: 'slide',
      backgroundTransition: 'fade',
      controls: true,
      progress: true,
      center: true,
    }});
  </script>
</body>
</html>
"""

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Created: {out}")


def main():
    parser = argparse.ArgumentParser(description="Generate Reveal.js HTML presentation")
    parser.add_argument("--output", default=str(Path("output/advanced/revealjs_presentation.html")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    generate_html(args.output, data)


if __name__ == "__main__":
    main()

