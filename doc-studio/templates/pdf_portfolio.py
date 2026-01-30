#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ポートフォリオPDFテンプレート
- クリエイティブでビジュアル重視
- カラー: モノクロ + アクセント
- 用途: デザイナー作品集、写真集
"""

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Portfolio</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    @page {
      size: 297mm 210mm; /* A4横 */
      margin: 0;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Noto Sans JP', sans-serif;
      color: #333;
    }

    /* 表紙 */
    .cover {
      width: 297mm;
      height: 210mm;
      background: #111;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      page-break-after: always;
      position: relative;
    }

    .cover-name {
      font-size: 48pt;
      font-weight: 300;
      color: #fff;
      letter-spacing: 0.5em;
      margin-bottom: 1cm;
    }

    .cover-title {
      font-size: 12pt;
      color: #666;
      letter-spacing: 0.3em;
    }

    /* プロフィールページ */
    .profile-page {
      width: 297mm;
      height: 210mm;
      padding: 15mm;
      page-break-after: always;
      display: grid;
      grid-template-columns: 1fr 1.5fr;
      gap: 15mm;
    }

    .profile-image {
      background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #999;
    }

    .profile-content h2 {
      font-size: 24pt;
      font-weight: 300;
      margin-bottom: 1cm;
    }

    .profile-content p {
      font-size: 10pt;
      line-height: 2;
      color: #666;
      margin-bottom: 1cm;
    }

    .skills {
      margin-top: 1cm;
    }

    .skill-item {
      display: flex;
      align-items: center;
      margin-bottom: 0.5cm;
    }

    .skill-name {
      width: 3cm;
      font-size: 10pt;
    }

    .skill-bar {
      flex: 1;
      height: 3px;
      background: #eee;
    }

    .skill-level {
      height: 100%;
      background: #111;
    }

    /* 作品ページ */
    .work-page {
      width: 297mm;
      height: 210mm;
      page-break-after: always;
      display: grid;
      grid-template-columns: 2fr 1fr;
    }

    .work-image {
      background: #f5f5f5;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #999;
      font-size: 14pt;
    }

    .work-info {
      padding: 15mm;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .work-number {
      font-size: 48pt;
      font-weight: 300;
      color: #eee;
      margin-bottom: 1cm;
    }

    .work-title {
      font-size: 20pt;
      font-weight: 500;
      margin-bottom: 0.5cm;
    }

    .work-category {
      font-size: 10pt;
      color: #999;
      margin-bottom: 1cm;
    }

    .work-description {
      font-size: 10pt;
      line-height: 1.8;
      color: #666;
    }

    /* グリッドページ */
    .grid-page {
      width: 297mm;
      height: 210mm;
      padding: 10mm;
      page-break-after: always;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 5mm;
    }

    .grid-item {
      background: #f5f5f5;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #999;
    }

    /* コンタクトページ */
    .contact-page {
      width: 297mm;
      height: 210mm;
      background: #111;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #fff;
    }

    .contact-page h2 {
      font-size: 24pt;
      font-weight: 300;
      margin-bottom: 1.5cm;
      letter-spacing: 0.3em;
    }

    .contact-info {
      text-align: center;
      line-height: 2;
      font-size: 11pt;
      color: #999;
    }
  </style>
</head>
<body>

<!-- 表紙 -->
<div class="cover">
  <div class="cover-name">YAMADA TARO</div>
  <div class="cover-title">PORTFOLIO 2026</div>
</div>

<!-- プロフィール -->
<div class="profile-page">
  <div class="profile-image">[Profile Photo]</div>
  <div class="profile-content">
    <h2>About Me</h2>
    <p>
      グラフィックデザイナー / アートディレクター<br>
      東京を拠点に、ブランディングからウェブデザインまで<br>
      幅広く活動しています。
    </p>
    <p>
      ミニマルで機能的なデザインを得意とし、<br>
      クライアントのビジョンを視覚化することに情熱を持っています。
    </p>
    <div class="skills">
      <div class="skill-item">
        <span class="skill-name">Branding</span>
        <div class="skill-bar"><div class="skill-level" style="width: 90%"></div></div>
      </div>
      <div class="skill-item">
        <span class="skill-name">Web Design</span>
        <div class="skill-bar"><div class="skill-level" style="width: 85%"></div></div>
      </div>
      <div class="skill-item">
        <span class="skill-name">UI/UX</span>
        <div class="skill-bar"><div class="skill-level" style="width: 80%"></div></div>
      </div>
    </div>
  </div>
</div>

<!-- 作品1 -->
<div class="work-page">
  <div class="work-image">[Work Image 1]</div>
  <div class="work-info">
    <div class="work-number">01</div>
    <div class="work-title">Project Alpha</div>
    <div class="work-category">Branding / Identity</div>
    <div class="work-description">
      テックスタートアップのブランディングプロジェクト。<br>
      ロゴデザイン、ビジュアルアイデンティティ、<br>
      ウェブサイトの総合的なデザインを担当。
    </div>
  </div>
</div>

<!-- 作品2 -->
<div class="work-page">
  <div class="work-image">[Work Image 2]</div>
  <div class="work-info">
    <div class="work-number">02</div>
    <div class="work-title">Project Beta</div>
    <div class="work-category">Web Design</div>
    <div class="work-description">
      コーポレートウェブサイトのリニューアル。<br>
      モダンでミニマルなデザインで、<br>
      ユーザーエクスペリエンスを大幅に改善。
    </div>
  </div>
</div>

<!-- グリッド -->
<div class="grid-page">
  <div class="grid-item">[Work 3]</div>
  <div class="grid-item">[Work 4]</div>
  <div class="grid-item">[Work 5]</div>
  <div class="grid-item">[Work 6]</div>
  <div class="grid-item">[Work 7]</div>
  <div class="grid-item">[Work 8]</div>
</div>

<!-- コンタクト -->
<div class="contact-page">
  <h2>GET IN TOUCH</h2>
  <div class="contact-info">
    hello@yamadataro.example.com<br>
    www.yamadataro.example.com<br>
    @yamadataro_design
  </div>
</div>

</body>
</html>
'''

import argparse
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright


def _load_data(args: argparse.Namespace) -> dict:
    if args.data and args.data_file:
        raise SystemExit("Use either --data or --data-file (not both)")

    if args.data_file:
        p = Path(args.data_file)
        return json.loads(p.read_text(encoding="utf-8"))

    if args.data:
        return json.loads(args.data)

    return {}


async def generate_pdf(output_path: str, _data: dict | None = None):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(HTML_CONTENT)
        await page.wait_for_timeout(2000)
        await page.pdf(
            path=str(output),
            width="297mm",
            height="210mm",
            print_background=True,
        )
        await browser.close()

    print(f"Created: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate portfolio PDF (Playwright)")
    parser.add_argument("--output", default=str(Path("output/pdf/03_portfolio.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    asyncio.run(generate_pdf(args.output, data))


if __name__ == "__main__":
    main()
