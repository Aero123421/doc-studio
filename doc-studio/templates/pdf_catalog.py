#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
カタログ/パンフレットPDFテンプレート
- ビジュアル重視のレイアウト
- カラー: ブラック + ゴールド（高級感）
- 用途: 製品カタログ、サービス案内
"""

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>カタログ</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap" rel="stylesheet">
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
      color: #333;
    }

    /* カバー */
    .cover {
      width: 210mm;
      height: 297mm;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      page-break-after: always;
      position: relative;
      overflow: hidden;
    }

    .cover::before {
      content: '';
      position: absolute;
      width: 400mm;
      height: 400mm;
      background: radial-gradient(circle, rgba(201,162,39,0.1) 0%, transparent 70%);
      top: -100mm;
      left: -100mm;
    }

    .cover-logo {
      font-size: 14pt;
      color: #c9a227;
      letter-spacing: 0.5em;
      margin-bottom: 2cm;
    }

    .cover h1 {
      font-size: 36pt;
      color: #fff;
      font-weight: 300;
      letter-spacing: 0.2em;
      margin-bottom: 1cm;
    }

    .cover-subtitle {
      font-size: 12pt;
      color: #c9a227;
      letter-spacing: 0.3em;
    }

    .cover-year {
      position: absolute;
      bottom: 3cm;
      font-size: 10pt;
      color: #666;
    }

    /* 商品ページ */
    .product-page {
      width: 210mm;
      height: 297mm;
      padding: 15mm;
      page-break-after: always;
      position: relative;
    }

    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 5mm;
      border-bottom: 1px solid #c9a227;
      margin-bottom: 10mm;
    }

    .brand-name {
      font-size: 10pt;
      color: #1a1a2e;
      font-weight: 600;
      letter-spacing: 0.2em;
    }

    .page-number {
      font-size: 9pt;
      color: #999;
    }

    /* 商品グリッド */
    .product-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10mm;
    }

    .product-card {
      border: 1px solid #eee;
      padding: 8mm;
    }

    .product-image {
      width: 100%;
      height: 60mm;
      background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
      margin-bottom: 5mm;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #999;
      font-size: 10pt;
    }

    .product-category {
      font-size: 9pt;
      color: #c9a227;
      letter-spacing: 0.1em;
      margin-bottom: 2mm;
    }

    .product-name {
      font-size: 14pt;
      font-weight: 600;
      color: #1a1a2e;
      margin-bottom: 3mm;
    }

    .product-description {
      font-size: 9pt;
      color: #666;
      line-height: 1.6;
      margin-bottom: 5mm;
    }

    .product-price {
      font-size: 16pt;
      font-weight: 600;
      color: #1a1a2e;
      text-align: right;
    }

    .product-price span {
      font-size: 10pt;
      font-weight: 400;
    }

    /* フルページ商品 */
    .product-full {
      display: grid;
      grid-template-columns: 1fr 1fr;
      height: calc(297mm - 40mm);
      gap: 10mm;
    }

    .product-full-image {
      background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #999;
    }

    .product-full-info {
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 10mm;
    }

    .product-full-category {
      font-size: 10pt;
      color: #c9a227;
      letter-spacing: 0.2em;
      margin-bottom: 1cm;
    }

    .product-full-name {
      font-size: 24pt;
      font-weight: 300;
      color: #1a1a2e;
      margin-bottom: 1cm;
      line-height: 1.3;
    }

    .product-full-description {
      font-size: 10pt;
      color: #666;
      line-height: 2;
      margin-bottom: 1.5cm;
    }

    .product-specs {
      border-top: 1px solid #eee;
      padding-top: 1cm;
    }

    .spec-row {
      display: flex;
      justify-content: space-between;
      padding: 3mm 0;
      border-bottom: 1px dotted #ddd;
      font-size: 9pt;
    }

    .spec-label {
      color: #999;
    }

    .spec-value {
      color: #333;
      font-weight: 500;
    }

    /* バックカバー */
    .back-cover {
      width: 210mm;
      height: 297mm;
      background: #1a1a2e;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      color: #fff;
    }

    .back-cover h2 {
      font-size: 18pt;
      font-weight: 300;
      letter-spacing: 0.3em;
      margin-bottom: 2cm;
    }

    .contact-info {
      font-size: 10pt;
      line-height: 2;
      color: #999;
    }

    .contact-info strong {
      color: #c9a227;
      font-weight: 500;
    }
  </style>
</head>
<body>

<!-- カバー -->
<div class="cover">
  <div class="cover-logo">PREMIUM COLLECTION</div>
  <h1>2026 SPRING</h1>
  <div class="cover-subtitle">CATALOG</div>
  <div class="cover-year">VOL.12</div>
</div>

<!-- 商品ページ1 - グリッド -->
<div class="product-page">
  <div class="page-header">
    <div class="brand-name">LUXE BRAND</div>
    <div class="page-number">02</div>
  </div>

  <div class="product-grid">
    <div class="product-card">
      <div class="product-image">[Product Image]</div>
      <div class="product-category">BAG</div>
      <div class="product-name">レザートートバッグ</div>
      <div class="product-description">上質なイタリアンレザーを使用した、シンプルで使いやすいトートバッグ。</div>
      <div class="product-price"><span>¥</span>45,000</div>
    </div>

    <div class="product-card">
      <div class="product-image">[Product Image]</div>
      <div class="product-category">ACCESSORY</div>
      <div class="product-name">シルクスカーフ</div>
      <div class="product-description">職人が一枚一枚手染めした、美しいグラデーションのシルクスカーフ。</div>
      <div class="product-price"><span>¥</span>18,000</div>
    </div>

    <div class="product-card">
      <div class="product-image">[Product Image]</div>
      <div class="product-category">WALLET</div>
      <div class="product-name">長財布</div>
      <div class="product-description">薄型設計でポケットにすっきり収まる、機能性とデザイン性を兼ね備えた長財布。</div>
      <div class="product-price"><span>¥</span>32,000</div>
    </div>

    <div class="product-card">
      <div class="product-image">[Product Image]</div>
      <div class="product-category">BAG</div>
      <div class="product-name">ミニショルダー</div>
      <div class="product-description">コンパクトでありながら必要な物がしっかり入る、軽量ショルダーバッグ。</div>
      <div class="product-price"><span>¥</span>28,000</div>
    </div>
  </div>
</div>

<!-- 商品ページ2 - フルページ -->
<div class="product-page">
  <div class="page-header">
    <div class="brand-name">LUXE BRAND</div>
    <div class="page-number">03</div>
  </div>

  <div class="product-full">
    <div class="product-full-image">[Feature Image]</div>
    <div class="product-full-info">
      <div class="product-full-category">SIGNATURE ITEM</div>
      <div class="product-full-name">アイコニック<br>ハンドバッグ</div>
      <div class="product-full-description">
        最高級の素材と職人の技が融合した、ブランドを代表するシグネチャーアイテム。
        時代を超えて愛される永遠のデザイン。
      </div>
      <div class="product-specs">
        <div class="spec-row">
          <span class="spec-label">素材</span>
          <span class="spec-value">イタリアンレザー</span>
        </div>
        <div class="spec-row">
          <span class="spec-label">サイズ</span>
          <span class="spec-value">W30 × H20 × D12cm</span>
        </div>
        <div class="spec-row">
          <span class="spec-label">重量</span>
          <span class="spec-value">480g</span>
        </div>
        <div class="spec-row">
          <span class="spec-label">価格</span>
          <span class="spec-value">¥128,000</span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- バックカバー -->
<div class="back-cover">
  <h2>LUXE BRAND</h2>
  <div class="contact-info">
    <strong>お問い合わせ</strong><br>
    〒100-0001 東京都千代田区1-1-1<br>
    TEL: 03-1234-5678<br>
    www.luxebrand.example.com
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
    parser = argparse.ArgumentParser(description="Generate catalog PDF (Playwright)")
    parser.add_argument("--output", default=str(Path("output/pdf/02_catalog.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    asyncio.run(generate_pdf(args.output, data))


if __name__ == "__main__":
    main()
