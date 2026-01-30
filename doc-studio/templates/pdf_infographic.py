#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
インフォグラフィックPDFテンプレート
- データ可視化重視
- カラー: ビビッドカラー
- 用途: 統計レポート、年次報告
"""

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Infographic Report</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4;
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

    .page {
      width: 210mm;
      height: 297mm;
      page-break-after: always;
      position: relative;
    }

    /* カバー */
    .cover {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: white;
      text-align: center;
    }

    .cover-year {
      font-size: 18pt;
      opacity: 0.8;
      margin-bottom: 1cm;
    }

    .cover h1 {
      font-size: 42pt;
      font-weight: 900;
      margin-bottom: 0.5cm;
    }

    .cover-subtitle {
      font-size: 14pt;
      font-weight: 400;
      opacity: 0.9;
    }

    /* データページ */
    .data-page {
      padding: 15mm;
      background: #f8f9fa;
    }

    .page-title {
      font-size: 24pt;
      font-weight: 700;
      color: #333;
      margin-bottom: 1cm;
      text-align: center;
    }

    /* ビッグナンバー */
    .big-numbers {
      display: flex;
      justify-content: space-around;
      margin: 1.5cm 0;
    }

    .big-number-item {
      text-align: center;
    }

    .big-number {
      font-size: 48pt;
      font-weight: 900;
      color: #667eea;
      line-height: 1;
    }

    .big-number-label {
      font-size: 11pt;
      color: #666;
      margin-top: 0.3cm;
    }

    /* バーチャート */
    .chart-container {
      background: white;
      padding: 1cm;
      border-radius: 10px;
      margin: 1cm 0;
      box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .chart-title {
      font-size: 14pt;
      font-weight: 700;
      color: #333;
      margin-bottom: 0.8cm;
    }

    .bar-chart {
      display: flex;
      flex-direction: column;
      gap: 0.5cm;
    }

    .bar-item {
      display: flex;
      align-items: center;
    }

    .bar-label {
      width: 3cm;
      font-size: 10pt;
      color: #666;
    }

    .bar-track {
      flex: 1;
      height: 25px;
      background: #f0f0f0;
      border-radius: 12px;
      overflow: hidden;
    }

    .bar-fill {
      height: 100%;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding-right: 10px;
      color: white;
      font-size: 10pt;
      font-weight: 700;
    }

    /* 円グラフ風 */
    .circle-stats {
      display: flex;
      justify-content: space-around;
      margin: 1.5cm 0;
    }

    .circle-item {
      text-align: center;
    }

    .circle-visual {
      width: 4cm;
      height: 4cm;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 0.5cm;
      color: white;
      font-size: 20pt;
      font-weight: 700;
    }

    .circle-label {
      font-size: 11pt;
      color: #666;
    }

    /* タイムライン */
    .timeline {
      position: relative;
      padding-left: 2cm;
    }

    .timeline::before {
      content: '';
      position: absolute;
      left: 0.5cm;
      top: 0;
      bottom: 0;
      width: 3px;
      background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    .timeline-item {
      position: relative;
      margin-bottom: 1cm;
      padding: 0.5cm;
      background: white;
      border-radius: 8px;
    }

    .timeline-item::before {
      content: '';
      position: absolute;
      left: -1.7cm;
      top: 0.8cm;
      width: 12px;
      height: 12px;
      background: #667eea;
      border-radius: 50%;
      border: 3px solid white;
    }

    .timeline-date {
      font-size: 10pt;
      color: #667eea;
      font-weight: 700;
      margin-bottom: 0.2cm;
    }

    .timeline-content {
      font-size: 11pt;
      color: #333;
    }

    /* グリッドカード */
    .grid-cards {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.8cm;
    }

    .info-card {
      background: white;
      padding: 0.8cm;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
      border-left: 4px solid #667eea;
    }

    .info-card-title {
      font-size: 11pt;
      font-weight: 700;
      color: #333;
      margin-bottom: 0.3cm;
    }

    .info-card-value {
      font-size: 24pt;
      font-weight: 900;
      color: #667eea;
      margin-bottom: 0.2cm;
    }

    .info-card-desc {
      font-size: 9pt;
      color: #999;
    }
  </style>
</head>
<body>

<!-- カバー -->
<div class="page cover">
  <div class="cover-year">2026</div>
  <h1>DATA REPORT</h1>
  <div class="cover-subtitle">Annual Statistics Overview</div>
</div>

<!-- ビッグナンバーページ -->
<div class="page data-page">
  <div class="page-title">Key Metrics</div>

  <div class="big-numbers">
    <div class="big-number-item">
      <div class="big-number">2.5M</div>
      <div class="big-number-label">Total Users</div>
    </div>
    <div class="big-number-item">
      <div class="big-number">+45%</div>
      <div class="big-number-label">Growth Rate</div>
    </div>
    <div class="big-number-item">
      <div class="big-number">98%</div>
      <div class="big-number-label">Satisfaction</div>
    </div>
  </div>

  <div class="grid-cards">
    <div class="info-card">
      <div class="info-card-title">Monthly Active Users</div>
      <div class="info-card-value">850K</div>
      <div class="info-card-desc">+23% from last year</div>
    </div>
    <div class="info-card">
      <div class="info-card-title">Revenue</div>
      <div class="info-card-value">¥1.2B</div>
      <div class="info-card-desc">+18% YoY growth</div>
    </div>
    <div class="info-card">
      <div class="info-card-title">Transactions</div>
      <div class="info-card-value">3.4M</div>
      <div class="info-card-desc">Daily average</div>
    </div>
    <div class="info-card">
      <div class="info-card-title">Retention</div>
      <div class="info-card-value">72%</div>
      <div class="info-card-desc">30-day retention</div>
    </div>
  </div>
</div>

<!-- チャートページ -->
<div class="page data-page">
  <div class="page-title">Growth Analysis</div>

  <div class="chart-container">
    <div class="chart-title">Sales by Quarter</div>
    <div class="bar-chart">
      <div class="bar-item">
        <div class="bar-label">Q1</div>
        <div class="bar-track">
          <div class="bar-fill" style="width: 65%; background: #667eea;">65%</div>
        </div>
      </div>
      <div class="bar-item">
        <div class="bar-label">Q2</div>
        <div class="bar-track">
          <div class="bar-fill" style="width: 78%; background: #764ba2;">78%</div>
        </div>
      </div>
      <div class="bar-item">
        <div class="bar-label">Q3</div>
        <div class="bar-track">
          <div class="bar-fill" style="width: 85%; background: #f093fb;">85%</div>
        </div>
      </div>
      <div class="bar-item">
        <div class="bar-label">Q4</div>
        <div class="bar-track">
          <div class="bar-fill" style="width: 92%; background: #f5576c;">92%</div>
        </div>
      </div>
    </div>
  </div>

  <div class="circle-stats">
    <div class="circle-item">
      <div class="circle-visual" style="background: #667eea;">A</div>
      <div class="circle-label">Category A<br>35%</div>
    </div>
    <div class="circle-item">
      <div class="circle-visual" style="background: #764ba2;">B</div>
      <div class="circle-label">Category B<br>28%</div>
    </div>
    <div class="circle-item">
      <div class="circle-visual" style="background: #f093fb;">C</div>
      <div class="circle-label">Category C<br>22%</div>
    </div>
    <div class="circle-item">
      <div class="circle-visual" style="background: #f5576c;">D</div>
      <div class="circle-label">Category D<br>15%</div>
    </div>
  </div>
</div>

<!-- タイムラインページ -->
<div class="page data-page">
  <div class="page-title">Year in Review</div>

  <div class="timeline">
    <div class="timeline-item">
      <div class="timeline-date">January 2026</div>
      <div class="timeline-content">New product launch - 10,000 users in first week</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">April 2026</div>
      <div class="timeline-content">Series B funding - ¥500M raised</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">July 2026</div>
      <div class="timeline-content">International expansion - 5 new markets</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">October 2026</div>
      <div class="timeline-content">1M users milestone reached</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">December 2026</div>
      <div class="timeline-content">Best quarter in company history</div>
    </div>
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
            format="A4",
            print_background=True,
        )
        await browser.close()

    print(f"Created: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate infographic PDF (Playwright)")
    parser.add_argument("--output", default=str(Path("output/pdf/04_infographic.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    asyncio.run(generate_pdf(args.output, data))


if __name__ == "__main__":
    main()
