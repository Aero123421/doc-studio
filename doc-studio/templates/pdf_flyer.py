#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
チラシ/フライヤーPDFテンプレート
- A4片面 or B5サイズ
- カラー: ビビッド
- 用途: イベント告知、プロモーション
"""

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Flyer</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    @page {
      size: 210mm 297mm;
      margin: 0;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Noto Sans JP', sans-serif;
    }

    /* A4チラシ - 縦 */
    .flyer {
      width: 210mm;
      height: 297mm;
      position: relative;
      overflow: hidden;
    }

    /* ヘッダー帯 */
    .flyer-header {
      height: 40mm;
      background: #ff6b6b;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      position: relative;
    }

    .flyer-badge {
      position: absolute;
      top: 10mm;
      right: 10mm;
      width: 25mm;
      height: 25mm;
      background: #ffd93d;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #333;
      font-size: 10pt;
      font-weight: 700;
      transform: rotate(15deg);
    }

    .flyer-title {
      font-size: 32pt;
      font-weight: 900;
      letter-spacing: 0.1em;
    }

    /* メインコンテンツ */
    .flyer-main {
      padding: 10mm;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10mm;
    }

    .flyer-image {
      height: 80mm;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 14pt;
      border-radius: 8px;
    }

    .flyer-info {
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .flyer-event-name {
      font-size: 20pt;
      font-weight: 700;
      color: #333;
      margin-bottom: 5mm;
    }

    .flyer-details {
      font-size: 11pt;
      color: #666;
      line-height: 2;
    }

    .flyer-details strong {
      color: #ff6b6b;
      display: inline-block;
      width: 2cm;
    }

    /* 特徴グリッド */
    .features {
      grid-column: 1 / -1;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 5mm;
      margin-top: 5mm;
    }

    .feature-item {
      background: #f8f9fa;
      padding: 8mm;
      border-radius: 8px;
      text-align: center;
      border-top: 3px solid #ff6b6b;
    }

    .feature-icon {
      width: 15mm;
      height: 15mm;
      background: #ff6b6b;
      border-radius: 50%;
      margin: 0 auto 4mm;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 14pt;
    }

    .feature-title {
      font-size: 12pt;
      font-weight: 700;
      color: #333;
      margin-bottom: 2mm;
    }

    .feature-desc {
      font-size: 9pt;
      color: #666;
    }

    /* フッター */
    .flyer-footer {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: #333;
      color: white;
      padding: 8mm 10mm;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .contact-info {
      font-size: 10pt;
      line-height: 1.8;
    }

    .qr-space {
      width: 25mm;
      height: 25mm;
      background: white;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #333;
      font-size: 8pt;
    }

    /* 割引バナー */
    .discount-banner {
      grid-column: 1 / -1;
      background: linear-gradient(90deg, #ffd93d 0%, #ff6b6b 100%);
      padding: 5mm;
      text-align: center;
      border-radius: 8px;
      margin-top: 5mm;
    }

    .discount-text {
      font-size: 16pt;
      font-weight: 700;
      color: white;
    }

    .discount-code {
      font-size: 12pt;
      color: #333;
      margin-top: 2mm;
    }
  </style>
</head>
<body>

<div class="flyer">
  <div class="flyer-header">
    <div class="flyer-title">GRAND OPENING</div>
    <div class="flyer-badge">NEW!</div>
  </div>

  <div class="flyer-main">
    <div class="flyer-image">[Event Image]</div>

    <div class="flyer-info">
      <div class="flyer-event-name">東京カフェ<br>グランドオープン</div>
      <div class="flyer-details">
        <strong>日時</strong>2026年2月15日(土)<br>
        <strong>時間</strong>10:00〜20:00<br>
        <strong>場所</strong>東京都渋谷区1-1-1<br>
        <strong>入場</strong>無料
      </div>
    </div>

    <div class="features">
      <div class="feature-item">
        <div class="feature-icon">★</div>
        <div class="feature-title">オリジナルコーヒー</div>
        <div class="feature-desc">厳選豆を使用した<br>特別ブレンド</div>
      </div>
      <div class="feature-item">
        <div class="feature-icon">♪</div>
        <div class="feature-title">ライブ演奏</div>
        <div class="feature-desc">アコースティック<br>ライブ開催</div>
      </div>
      <div class="feature-item">
        <div class="feature-icon">♥</div>
        <div class="feature-title">限定スイーツ</div>
        <div class="feature-desc">オープン記念<br>特別メニュー</div>
      </div>
    </div>

    <div class="discount-banner">
      <div class="discount-text">オープン記念！全品20% OFF</div>
      <div class="discount-code">クーポンコード: OPEN2026</div>
    </div>
  </div>

  <div class="flyer-footer">
    <div class="contact-info">
      <strong>東京カフェ</strong><br>
      TEL: 03-1234-5678<br>
      www.tokyocafe.example.com
    </div>
    <div class="qr-space">[QR Code]</div>
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
            width="210mm",
            height="297mm",
            print_background=True,
        )
        await browser.close()

    print(f"Created: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate flyer PDF (Playwright)")
    parser.add_argument("--output", default=str(Path("output/pdf/05_flyer.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    asyncio.run(generate_pdf(args.output, data))


if __name__ == "__main__":
    main()
