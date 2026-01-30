#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeasyPrintによる最高品質のPDF生成
- 最適化されたHTML/CSS
- 組版品質の高さ
- フォントサブセット化対応
"""

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>WeasyPrint Premium Document</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;600&display=swap" rel="stylesheet">
  <style>
    /* ページ設定 */
    @page {
      size: 210mm 297mm;
      margin: 20mm 25mm 25mm 25mm;

      @bottom-center {
        content: counter(page) " / " counter(pages);
        font-size: 9pt;
        color: #999;
        font-family: 'Noto Sans JP', sans-serif;
      }

      @top-left {
        content: "Premium Annual Report 2026";
        font-size: 8pt;
        color: #999;
        font-family: 'Noto Sans JP', sans-serif;
      }
    }

    @page:first {
      @bottom-center { content: none; }
      @top-left { content: none; }
    }

    @page cover {
      margin: 0;
      @bottom-center { content: none; }
      @top-left { content: none; }
    }

    /* 基本設定 */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Noto Sans JP', 'Hiragino Sans', sans-serif;
      font-size: 10.5pt;
      line-height: 1.8;
      color: #333;
      orphans: 3;
      widows: 3;
    }

    /* カバーページ */
    .cover {
      page: cover;
      width: 210mm;
      height: 297mm;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      color: white;
      position: relative;
      overflow: hidden;
    }

    .cover::before {
      content: '';
      position: absolute;
      width: 600mm;
      height: 600mm;
      background: radial-gradient(circle, rgba(201,162,39,0.15) 0%, transparent 60%);
      top: -200mm;
      left: -200mm;
    }

    .cover-logo {
      font-size: 12pt;
      letter-spacing: 0.8em;
      color: #c9a227;
      margin-bottom: 2cm;
      text-transform: uppercase;
    }

    .cover h1 {
      font-family: 'Noto Serif JP', serif;
      font-size: 42pt;
      font-weight: 600;
      line-height: 1.3;
      margin-bottom: 1cm;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .cover-subtitle {
      font-size: 14pt;
      font-weight: 300;
      opacity: 0.9;
      margin-bottom: 3cm;
    }

    .cover-meta {
      font-size: 10pt;
      opacity: 0.7;
      line-height: 2;
    }

    .cover-decoration {
      position: absolute;
      bottom: -50mm;
      right: -50mm;
      width: 300mm;
      height: 300mm;
      border: 1px solid rgba(201,162,39,0.3);
      border-radius: 50%;
    }

    /* セクションブレイク */
    .section-break {
      page-break-before: always;
    }

    /* 見出し */
    h1 {
      font-family: 'Noto Serif JP', serif;
      font-size: 22pt;
      font-weight: 600;
      color: #1a1a2e;
      margin-top: 0;
      margin-bottom: 1cm;
      padding-bottom: 0.5cm;
      border-bottom: 3px solid #c9a227;
      page-break-after: avoid;
    }

    h2 {
      font-size: 14pt;
      font-weight: 700;
      color: #0f3460;
      margin-top: 0.8cm;
      margin-bottom: 0.5cm;
      page-break-after: avoid;
    }

    h3 {
      font-size: 12pt;
      font-weight: 600;
      color: #533483;
      margin-top: 0.6cm;
      margin-bottom: 0.4cm;
      page-break-after: avoid;
    }

    /* 段落 */
    p {
      margin-bottom: 0.8em;
      text-align: justify;
      hyphens: auto;
    }

    /* リード文 */
    .lead {
      font-size: 12pt;
      font-weight: 300;
      color: #555;
      line-height: 1.9;
      margin-bottom: 1.5cm;
      padding: 0.5cm 0;
      border-top: 1px solid #eee;
      border-bottom: 1px solid #eee;
    }

    /* 引用 */
    blockquote {
      margin: 1cm 0;
      padding: 1cm 1.5cm;
      background: linear-gradient(90deg, #f8f9fa 0%, #fff 100%);
      border-left: 4px solid #c9a227;
      font-style: italic;
      color: #555;
    }

    blockquote cite {
      display: block;
      margin-top: 0.5cm;
      font-size: 9pt;
      color: #999;
      font-style: normal;
    }

    /* リスト */
    ul, ol {
      margin: 0.8cm 0;
      padding-left: 1.5cm;
    }

    li {
      margin-bottom: 0.3cm;
    }

    /* ハイライトボックス */
    .highlight-box {
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      border: 1px solid #dee2e6;
      border-radius: 8px;
      padding: 1cm;
      margin: 1cm 0;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .highlight-box h4 {
      color: #1a1a2e;
      font-size: 11pt;
      margin-bottom: 0.5cm;
      padding-bottom: 0.3cm;
      border-bottom: 2px solid #c9a227;
    }

    /* データカードグリッド */
    .data-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.8cm;
      margin: 1cm 0;
    }

    .data-card {
      background: white;
      border: 1px solid #e9ecef;
      border-radius: 8px;
      padding: 0.8cm;
      text-align: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .data-card-value {
      font-size: 24pt;
      font-weight: 700;
      color: #1a1a2e;
      display: block;
      margin-bottom: 0.2cm;
    }

    .data-card-label {
      font-size: 9pt;
      color: #666;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .data-card-change {
      font-size: 10pt;
      color: #28a745;
      margin-top: 0.3cm;
    }

    .data-card-change.negative {
      color: #dc3545;
    }

    /* テーブル */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1cm 0;
      font-size: 9.5pt;
    }

    thead {
      background: #1a1a2e;
      color: white;
    }

    th {
      padding: 0.4cm 0.5cm;
      text-align: left;
      font-weight: 600;
      text-transform: uppercase;
      font-size: 8.5pt;
      letter-spacing: 0.05em;
    }

    td {
      padding: 0.4cm 0.5cm;
      border-bottom: 1px solid #e9ecef;
    }

    tbody tr:nth-child(even) {
      background: #f8f9fa;
    }

    tbody tr:hover {
      background: #e9ecef;
    }

    /* 2カラムレイアウト */
    .two-column {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1cm;
      margin: 1cm 0;
    }

    .column {
      padding: 0.5cm;
    }

    /* ページ区切り */
    .page-break {
      page-break-after: always;
    }

    /* フットノート */
    .footnote {
      font-size: 8pt;
      color: #666;
      border-top: 1px solid #ddd;
      margin-top: 1cm;
      padding-top: 0.3cm;
    }

    /* 図表キャプション */
    figcaption {
      font-size: 9pt;
      color: #666;
      text-align: center;
      margin-top: 0.3cm;
      font-style: italic;
    }

    /* 装飾要素 */
    .drop-cap {
      float: left;
      font-size: 48pt;
      line-height: 1;
      padding-right: 0.2cm;
      color: #c9a227;
      font-family: 'Noto Serif JP', serif;
    }

    /* チャートプレースホルダー */
    .chart-container {
      background: #f8f9fa;
      border: 1px solid #dee2e6;
      border-radius: 8px;
      padding: 1cm;
      margin: 1cm 0;
      text-align: center;
    }

    .chart-bar {
      display: inline-block;
      margin: 0 0.2cm;
      background: linear-gradient(180deg, #1a1a2e 0%, #533483 100%);
      border-radius: 4px 4px 0 0;
      position: relative;
    }

    .chart-bar::after {
      content: attr(data-value);
      position: absolute;
      top: -20px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 9pt;
      color: #333;
    }

    /* タイムライン */
    .timeline {
      position: relative;
      padding-left: 2cm;
      margin: 1cm 0;
    }

    .timeline::before {
      content: '';
      position: absolute;
      left: 0.5cm;
      top: 0;
      bottom: 0;
      width: 2px;
      background: linear-gradient(180deg, #c9a227 0%, #1a1a2e 100%);
    }

    .timeline-item {
      position: relative;
      margin-bottom: 0.8cm;
      padding: 0.5cm;
      background: #f8f9fa;
      border-radius: 4px;
    }

    .timeline-item::before {
      content: '';
      position: absolute;
      left: -1.7cm;
      top: 0.6cm;
      width: 10px;
      height: 10px;
      background: #c9a227;
      border-radius: 50%;
      border: 2px solid white;
      box-shadow: 0 0 0 2px #c9a227;
    }

    .timeline-date {
      font-size: 9pt;
      color: #c9a227;
      font-weight: 600;
      margin-bottom: 0.2cm;
    }
  </style>
</head>
<body>

<!-- カバー -->
<div class="cover">
  <div class="cover-logo">Annual Report</div>
  <h1>Enterprise<br>Transformation<br>2026</h1>
  <div class="cover-subtitle">Strategic Vision & Performance Review</div>
  <div class="cover-meta">
    Prepared for Board of Directors<br>
    Fiscal Year 2025-2026
  </div>
  <div class="cover-decoration"></div>
</div>

<!-- エグゼクティブサマリー -->
<div class="section-break">
  <h1>Executive Summary</h1>

  <p class="lead">
    2025年度は、企業変革の重要な転換点となりました。デジタルトランスフォーメーションの
    完了とともに、新たな成長フェーズへの移行を成功させることができました。
  </p>

  <div class="data-grid">
    <div class="data-card">
      <span class="data-card-value">¥12.5B</span>
      <span class="data-card-label">総売上高</span>
      <div class="data-card-change">+23% YoY</div>
    </div>
    <div class="data-card">
      <span class="data-card-value">18.5%</span>
      <span class="data-card-label">営業利益率</span>
      <div class="data-card-change">+2.3pp</div>
    </div>
    <div class="data-card">
      <span class="data-card-value">2,450</span>
      <span class="data-card-label">従業員数</span>
      <div class="data-card-change">+12%</div>
    </div>
  </div>

  <blockquote>
    "変革は終わりではなく、新しい始まりである。私たちはこれからも挑戦を続ける。"
    <cite>— CEO 山田太郎</cite>
  </blockquote>
</div>

<!-- ビジネスハイライト -->
<div class="section-break">
  <h1>Business Highlights</h1>

  <h2>市場拡大戦略</h2>

  <p>
    <span class="drop-cap">今</span>年度は、国内市場での地位確固に加え、
    海外市場への積極的な展開を推進しました。特にアジア太平洋地域での
    事業拡大は、予想を上回る成果を上げています。
  </p>

  <div class="highlight-box">
    <h4>主要成果</h4>
    <ul>
      <li>シンガポール・バンコクに新規事務所を開設</li>
      <li>現地パートナーとの戦略的提携を3件締結</li>
      <li>海外売上比率が前年比8%から15%に向上</li>
      <li>グローバル展開に必要な人材を50名採用</li>
    </ul>
  </div>

  <h2>イノベーション</h2>

  <div class="two-column">
    <div class="column">
      <h3>テクノロジー投資</h3>
      <p>
        AI・機械学習技術を活用した業務自動化を推進。
        顧客対応、在庫管理、需要予測の3分野でシステムを導入し、
        業務効率が平均30%向上しました。
      </p>
    </div>
    <div class="column">
      <h3>サステナビリティ</h3>
      <p>
        2030年カーボンニュートラル達成に向け、
        再生可能エネルギーへの切り替えを加速。
        現在の電力使用量の65%をクリーンエネルギーで賄っています。
      </p>
    </div>
  </div>
</div>

<!-- 財務パフォーマンス -->
<div class="section-break">
  <h1>Financial Performance</h1>

  <h2>四半期業績</h2>

  <table>
    <thead>
      <tr>
        <th>四半期</th>
        <th>売上高</th>
        <th>営業利益</th>
        <th>営業利益率</th>
        <th>前年比</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Q1 2025</td>
        <td>¥2.8B</td>
        <td>¥420M</td>
        <td>15.0%</td>
        <td>+8%</td>
      </tr>
      <tr>
        <td>Q2 2025</td>
        <td>¥3.1B</td>
        <td>¥520M</td>
        <td>16.8%</td>
        <td>+12%</td>
      </tr>
      <tr>
        <td>Q3 2025</td>
        <td>¥3.3B</td>
        <td>¥610M</td>
        <td>18.5%</td>
        <td>+18%</td>
      </tr>
      <tr>
        <td>Q4 2025</td>
        <td>¥3.3B</td>
        <td>¥640M</td>
        <td>19.4%</td>
        <td>+22%</td>
      </tr>
    </tbody>
  </table>

  <h2>重要マイルストーン</h2>

  <div class="timeline">
    <div class="timeline-item">
      <div class="timeline-date">2025年4月</div>
      <div>新経営体制発足、中期経営計画の策定完了</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">2025年7月</div>
      <div>シンガポール事務所開設、アジア展開本格化</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">2025年10月</div>
      <div>AI予測システム本番稼働、業務効率が30%向上</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-date">2026年1月</div>
      <div>通期決算発表、過去最高益を達成</div>
    </div>
  </div>
</div>

<!-- 今後の展望 -->
<div class="section-break">
  <h1>Future Outlook</h1>

  <p class="lead">
    2026年度は、引き続き成長投資を加速させながら、
    収益性のさらなる向上を目指します。
  </p>

  <div class="highlight-box">
    <h4>2026年度 優先戦略</h4>
    <ol>
      <li>北米市場への事業展開（ニューヨーク事務所開設予定）</li>
      <li>新規事業領域への投資（フィンテック分野）</li>
      <li>人材育成プログラムの拡充（年間100名の新卒採用）</li>
      <li>カーボンニュートラル達成に向けた投資拡大</li>
    </ol>
  </div>

  <div class="footnote">
    本資料は機密情報を含みます。無断での複製・配布を禁じます。<br>
    © 2026 Enterprise Inc. All rights reserved.
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
    """WeasyPrintを試し、失敗したらPlaywrightへフォールバックしてPDF生成"""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        from weasyprint import HTML

        HTML(string=HTML_CONTENT).write_pdf(str(output))
        print(f"Created (WeasyPrint): {output}")
        return

    except Exception as e:
        print(f"WeasyPrint error: {e}")
        print("Falling back to Playwright...")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(HTML_CONTENT)
        await page.wait_for_timeout(3000)
        await page.pdf(
            path=str(output),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()

    print(f"Created (Playwright fallback): {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate premium PDF (WeasyPrint/Playwright)")
    parser.add_argument("--output", default=str(Path("output/advanced/02_weasyprint_premium.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    asyncio.run(generate_pdf(args.output, data))


if __name__ == "__main__":
    main()
