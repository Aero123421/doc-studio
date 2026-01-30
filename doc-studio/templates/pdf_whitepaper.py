#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ホワイトペーパーPDFテンプレート
- プロフェッショナルな文書レイアウト
- カラー: ネイビー + グレー
- 用途: 技術文書、調査報告書
"""

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ホワイトペーパー</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;600&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4;
      margin: 2.5cm 2cm;
      @bottom-center {
        content: counter(page);
        font-size: 10pt;
        color: #666;
      }
    }

    @page:first {
      @bottom-center { content: none; }
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Noto Sans JP', sans-serif;
      font-size: 11pt;
      line-height: 1.8;
      color: #333;
    }

    /* 表紙 */
    .cover {
      page-break-after: always;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 0 1cm;
    }

    .cover-badge {
      display: inline-block;
      background: #1e3a5f;
      color: white;
      padding: 0.3cm 0.8cm;
      font-size: 10pt;
      font-weight: 500;
      margin-bottom: 1.5cm;
      width: fit-content;
    }

    .cover h1 {
      font-family: 'Noto Serif JP', serif;
      font-size: 28pt;
      font-weight: 600;
      color: #1e3a5f;
      line-height: 1.4;
      margin-bottom: 1cm;
    }

    .cover-subtitle {
      font-size: 14pt;
      color: #666;
      margin-bottom: 2cm;
    }

    .cover-meta {
      font-size: 10pt;
      color: #999;
      border-top: 1px solid #ddd;
      padding-top: 0.5cm;
    }

    /* 目次 */
    .toc {
      page-break-after: always;
    }

    .toc h2 {
      font-size: 18pt;
      color: #1e3a5f;
      margin-bottom: 1cm;
      padding-bottom: 0.3cm;
      border-bottom: 2px solid #1e3a5f;
    }

    .toc-item {
      display: flex;
      justify-content: space-between;
      padding: 0.4cm 0;
      border-bottom: 1px dotted #ccc;
    }

    .toc-number {
      color: #1e3a5f;
      font-weight: 600;
      margin-right: 0.5cm;
    }

    /* 見出し */
    h2 {
      font-size: 16pt;
      color: #1e3a5f;
      margin-top: 1.5cm;
      margin-bottom: 0.8cm;
      padding-bottom: 0.3cm;
      border-bottom: 2px solid #1e3a5f;
      page-break-after: avoid;
    }

    h3 {
      font-size: 13pt;
      color: #333;
      margin-top: 1cm;
      margin-bottom: 0.5cm;
      page-break-after: avoid;
    }

    h4 {
      font-size: 11pt;
      color: #555;
      margin-top: 0.8cm;
      margin-bottom: 0.4cm;
    }

    /* 本文 */
    p {
      margin-bottom: 0.8cm;
      text-align: justify;
    }

    /* 引用 */
    blockquote {
      margin: 1cm 0;
      padding: 0.8cm 1cm;
      background: #f5f5f5;
      border-left: 4px solid #1e3a5f;
      font-style: italic;
    }

    /* 箇条書き */
    ul, ol {
      margin: 0.8cm 0;
      padding-left: 1.2cm;
    }

    li {
      margin-bottom: 0.3cm;
    }

    /* 表 */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1cm 0;
      font-size: 10pt;
    }

    th {
      background: #1e3a5f;
      color: white;
      padding: 0.4cm;
      text-align: left;
      font-weight: 500;
    }

    td {
      padding: 0.4cm;
      border-bottom: 1px solid #ddd;
    }

    tr:nth-child(even) {
      background: #f9f9f9;
    }

    /* コード */
    code {
      font-family: 'Consolas', monospace;
      background: #f4f4f4;
      padding: 0.1cm 0.3cm;
      font-size: 10pt;
      border-radius: 3px;
    }

    pre {
      background: #2d2d2d;
      color: #f8f8f2;
      padding: 0.8cm;
      overflow-x: auto;
      font-size: 9pt;
      line-height: 1.5;
      margin: 1cm 0;
    }

    pre code {
      background: none;
      padding: 0;
      color: inherit;
    }

    /* 図表キャプション */
    .figure {
      margin: 1cm 0;
      text-align: center;
    }

    .figure-caption {
      font-size: 10pt;
      color: #666;
      margin-top: 0.3cm;
    }

    /* キーポイントボックス */
    .key-point {
      background: #e8f0f8;
      border: 1px solid #1e3a5f;
      padding: 0.8cm;
      margin: 1cm 0;
    }

    .key-point-title {
      font-weight: 600;
      color: #1e3a5f;
      margin-bottom: 0.3cm;
    }

    /* 脚注 */
    .footnote {
      font-size: 9pt;
      color: #666;
      border-top: 1px solid #ddd;
      margin-top: 1cm;
      padding-top: 0.3cm;
    }
  </style>
</head>
<body>

<!-- 表紙 -->
<div class="cover">
  <div class="cover-badge">WHITE PAPER</div>
  <h1>デジタルトランスフォーメーションの現状と未来<br>〜企業変革のための戦略的アプローチ〜</h1>
  <div class="cover-subtitle">Digital Transformation Strategy for Enterprise Growth</div>
  <div class="cover-meta">
    発行：株式会社サンプル<br>
    発行日：2026年1月<br>
    バージョン：1.0
  </div>
</div>

<!-- 目次 -->
<div class="toc">
  <h2>目次</h2>
  <div class="toc-item">
    <span><span class="toc-number">1.</span>はじめに</span>
    <span>3</span>
  </div>
  <div class="toc-item">
    <span><span class="toc-number">2.</span>DXの現状分析</span>
    <span>4</span>
  </div>
  <div class="toc-item">
    <span><span class="toc-number">3.</span>成功事例の研究</span>
    <span>6</span>
  </div>
  <div class="toc-item">
    <span><span class="toc-number">4.</span>戦略フレームワーク</span>
    <span>8</span>
  </div>
  <div class="toc-item">
    <span><span class="toc-number">5.</span>今後の展望</span>
    <span>10</span>
  </div>
</div>

<!-- 本文 -->
<h2>1. はじめに</h2>
<p>
デジタルトランスフォーメーション（DX）は、単なる技術導入ではなく、企業のビジネスモデル、組織文化、プロセスを根本から見直す変革である。本ホワイトペーパーでは、DXの現状と課題、そして成功に導くための戦略的アプローチを提唱する。
</p>

<blockquote>
「DXは目的地ではなく、旅である。重要なのは、継続的な改善と学習の文化を構築することだ。」
</blockquote>

<h2>2. DXの現状分析</h2>
<h3>2.1 市場動向</h3>
<p>
2025年のDX市場規模は前年比15%増の12兆円に達した。特に、クラウド移行とAI活用が主要な投資領域となっている。
</p>

<table>
  <tr>
    <th>投資領域</th>
    <th>市場規模</th>
    <th>成長率</th>
  </tr>
  <tr>
    <td>クラウドインフラ</td>
    <td>4.2兆円</td>
    <td>+22%</td>
  </tr>
  <tr>
    <td>AI・機械学習</td>
    <td>2.8兆円</td>
    <td>+35%</td>
  </tr>
  <tr>
    <td>サイバーセキュリティ</td>
    <td>1.9兆円</td>
    <td>+18%</td>
  </tr>
</table>

<h3>2.2 企業の課題</h3>
<ul>
  <li>レガシーシステムの老朽化と保守コストの増大</li>
  <li>デジタル人材の不足と採用難</li>
  <li>部門間のサイロ化によるデータ活用の遅れ</li>
  <li>投資対効果の測定困難さ</li>
</ul>

<h2>3. 成功事例の研究</h2>

<div class="key-point">
  <div class="key-point-title">Key Point: 成功の共通要素</div>
  <p>
    DXに成功した企業には以下の共通点が見られた：
    ①経営層の強いコミットメント
    ②明確なビジョンとロードマップ
    ③アジャイルな開発アプローチ
    ④人材育成への投資
  </p>
</div>

<h2>4. 戦略フレームワーク</h2>
<h3>4.1 4Pフレームワーク</h3>
<p>
本報告書では、以下の4Pフレームワークを提案する：
</p>
<ol>
  <li><strong>People（人材）：</strong>デジタルリテラシーの向上と人材育成</li>
  <li><strong>Process（プロセス）：</strong>業務プロセスの標準化と自動化</li>
  <li><strong>Platform（プラットフォーム）：</strong>統合基盤の構築</li>
  <li><strong>Partnership（パートナーシップ）：</strong>エコシステムの形成</li>
</ol>

<h2>5. 今後の展望</h2>
<p>
DXは今後も加速し、2030年には現在の3倍規模に達すると予想される。企業は、技術への投資と並行して、組織文化の変革にも注力する必要がある。
</p>

<div class="footnote">
  ※本資料の内容は、公開情報および調査結果に基づくものです。<br>
  ※掲載のデータは予告なく変更される場合があります。
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
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()

    print(f"Created: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate whitepaper PDF (Playwright)")
    parser.add_argument("--output", default=str(Path("output/pdf/01_whitepaper.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    asyncio.run(generate_pdf(args.output, data))


if __name__ == "__main__":
    main()
