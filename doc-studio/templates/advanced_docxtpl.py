#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docxtplによる高度なWordテンプレート生成
- Jinja2テンプレートエンジン
- 動的データ挿入
- 複雑な条件分岐とループ
- 企業レベルのドキュメント自動生成
"""

import argparse
import json
from pathlib import Path

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import datetime
import random

# サンプルデータ - 実際にはAPIやDBから取得
data = {
    'company_name': 'テクノロジー・イノベーション株式会社',
    'company_address': '東京都千代田区丸の内1-1-1',
    'company_tel': '03-1234-5678',
    'document_title': 'プロジェクト提案書',
    'document_subtitle': 'AI駆動型業務自動化システム導入案',
    'document_date': datetime.date.today().strftime('%Y年%m月%d日'),
    'document_version': 'v2.1',
    'client_name': 'ABC商事株式会社',
    'client_contact': '山田 太郎 様',
    'project_name': 'AI業務自動化プラットフォーム構築',
    'project_duration': '6ヶ月',
    'project_budget': '¥45,000,000',
    'executive_summary': '''
    本提案書では、貴社の業務効率化を目的としたAI駆動型自動化システムの
    導入についてご提案いたします。最新の機械学習技術を活用し、
    反復的な業務を80%削減し、従業員の創造的業務への注力を実現します。
    ''',
    'team_members': [
        {'name': '佐藤 健一', 'role': 'プロジェクトマネージャー', 'experience': '15年', 'cert': 'PMP'},
        {'name': '田中 美咲', 'role': 'AIエンジニア', 'experience': '8年', 'cert': 'TensorFlow認定'},
        {'name': '鈴木 大輔', 'role': 'システムアーキテクト', 'experience': '12年', 'cert': 'AWS SA'},
        {'name': '高橋 由美', 'role': 'データサイエンティスト', 'experience': '6年', 'cert': '統計検定1級'},
    ],
    'milestones': [
        {'phase': '第1フェーズ', 'task': '要件定義・環境構築', 'duration': '1ヶ月', 'deliverable': '要件定義書、環境設計書'},
        {'phase': '第2フェーズ', 'task': 'データ収集・前処理', 'duration': '1.5ヶ月', 'deliverable': 'データパイプライン、クレンジング済みデータ'},
        {'phase': '第3フェーズ', 'task': 'AIモデル開発', 'duration': '2ヶ月', 'deliverable': '学習済みモデル、精度検証レポート'},
        {'phase': '第4フェーズ', 'task': 'システム統合・テスト', 'duration': '1.5ヶ月', 'deliverable': '統合システム、テスト結果報告書'},
    ],
    'cost_breakdown': [
        {'item': '要件定義・設計', 'cost': 4500000, 'note': 'ワークショップ含む'},
        {'item': 'インフラ構築', 'cost': 8000000, 'note': 'クラウド環境'},
        {'item': 'AIモデル開発', 'cost': 15000000, 'note': 'カスタムモデル'},
        {'item': 'システム開発', 'cost': 12000000, 'note': 'フロント・バックエンド'},
        {'item': 'テスト・検証', 'cost': 3500000, 'note': '包括的テスト'},
        {'item': '保守・サポート(1年)', 'cost': 2000000, 'note': '24時間対応'},
    ],
    'risks': [
        {'risk': 'データ品質不良', 'impact': '高', 'probability': '中', 'mitigation': '事前データ監査・クレンジング強化'},
        {'risk': 'モデル精度不足', 'impact': '高', 'probability': '低', 'mitigation': '段階的学習・追加データ収集'},
        {'risk': '統合遅延', 'impact': '中', 'probability': '中', 'mitigation': '早期検証・リスク予備費設定'},
    ],
    'benefits': [
        {'metric': '業務時間削減', 'value': '80%', 'description': '反復的タスクの自動化により'},
        {'metric': 'エラー率削減', 'value': '95%', 'description': '人為的ミスの排除'},
        {'metric': '処理速度向上', 'value': '10x', 'description': '並列処理による高速化'},
        {'metric': 'ROI', 'value': '300%', 'description': '2年間での投資回収率'},
    ],
    'show_detailed_cost': True,
    'include_case_study': True,
    'case_studies': [
        {'company': 'XYZ製造株式会社', 'industry': '製造業', 'result': '生産計画業務を75%短縮'},
        {'company': 'DEF物流株式会社', 'industry': '物流業', 'result': '配送最適化でコスト30%削減'},
    ],
    'approval_name': 'プロジェクト承認者',
    'approval_date': '___年___月___日',
}

# テンプレートHTML（Jinja2形式）
TEMPLATE_CONTENT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ document_title }}</title>
    <style>
        body {
            font-family: "Noto Sans JP", "Hiragino Sans", sans-serif;
            font-size: 11pt;
            line-height: 1.8;
            color: #333;
        }
        .cover {
            page-break-after: always;
            text-align: center;
            padding-top: 200px;
        }
        .cover-title {
            font-size: 28pt;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 20px;
            border-bottom: 4px solid #c9a227;
            padding-bottom: 20px;
        }
        .cover-subtitle {
            font-size: 16pt;
            color: #555;
            margin-bottom: 100px;
        }
        .cover-meta {
            font-size: 12pt;
            color: #666;
            line-height: 2;
        }
        h1 {
            font-size: 18pt;
            color: #1a365d;
            border-left: 5px solid #c9a227;
            padding-left: 15px;
            margin-top: 30px;
            page-break-after: avoid;
        }
        h2 {
            font-size: 14pt;
            color: #2c5282;
            margin-top: 25px;
            page-break-after: avoid;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 10pt;
        }
        th {
            background-color: #1a365d;
            color: white;
            padding: 12px;
            text-align: left;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .highlight-box {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            border: 2px solid #c9a227;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        .metric-card {
            background: #1a365d;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-value {
            font-size: 24pt;
            font-weight: bold;
            color: #c9a227;
        }
        .signature {
            margin-top: 50px;
            text-align: right;
        }
        .signature-line {
            border-top: 1px solid #333;
            width: 300px;
            display: inline-block;
            margin-top: 50px;
            padding-top: 5px;
        }
    </style>
</head>
<body>

<!-- カバーページ -->
<div class="cover">
    <div class="cover-title">{{ document_title }}</div>
    <div class="cover-subtitle">{{ document_subtitle }}</div>
    <div class="cover-meta">
        <p><strong>提案先:</strong> {{ client_name }}</p>
        <p><strong>ご担当:</strong> {{ client_contact }}</p>
        <p><strong>提案元:</strong> {{ company_name }}</p>
        <p><strong>日付:</strong> {{ document_date }}</p>
        <p><strong>バージョン:</strong> {{ document_version }}</p>
    </div>
</div>

<!-- エグゼクティブサマリー -->
<h1>1. エグゼクティブサマリー</h1>
<p>{{ executive_summary }}</p>

<div class="highlight-box">
    <h2>プロジェクト概要</h2>
    <p><strong>プロジェクト名:</strong> {{ project_name }}</p>
    <p><strong>期間:</strong> {{ project_duration }}</p>
    <p><strong>予算:</strong> {{ project_budget }}</p>
</div>

<!-- 期待効果 -->
<h1>2. 期待効果</h1>
<div class="metric-grid">
    {% for benefit in benefits %}
    <div class="metric-card">
        <div class="metric-value">{{ benefit.value }}</div>
        <div>{{ benefit.metric }}</div>
        <div style="font-size: 9pt; opacity: 0.8;">{{ benefit.description }}</div>
    </div>
    {% endfor %}
</div>

<!-- チーム構成 -->
<h1>3. プロジェクトチーム</h1>
<table>
    <tr>
        <th>氏名</th>
        <th>役割</th>
        <th>経験年数</th>
        <th>資格</th>
    </tr>
    {% for member in team_members %}
    <tr>
        <td>{{ member.name }}</td>
        <td>{{ member.role }}</td>
        <td>{{ member.experience }}</td>
        <td>{{ member.cert }}</td>
    </tr>
    {% endfor %}
</table>

<!-- スケジュール -->
<h1>4. プロジェクトスケジュール</h1>
<table>
    <tr>
        <th>フェーズ</th>
        <th>タスク</th>
        <th>期間</th>
        <th>成果物</th>
    </tr>
    {% for milestone in milestones %}
    <tr>
        <td>{{ milestone.phase }}</td>
        <td>{{ milestone.task }}</td>
        <td>{{ milestone.duration }}</td>
        <td>{{ milestone.deliverable }}</td>
    </tr>
    {% endfor %}
</table>

{% if show_detailed_cost %}
<!-- 費用明細 -->
<h1>5. 費用明細</h1>
<table>
    <tr>
        <th>項目</th>
        <th>金額</th>
        <th>備考</th>
    </tr>
    {% set total = 0 %}
    {% for item in cost_breakdown %}
    {% set total = total + item.cost %}
    <tr>
        <td>{{ item.item }}</td>
        <td style="text-align: right;">¥{{ "{:,}".format(item.cost) }}</td>
        <td>{{ item.note }}</td>
    </tr>
    {% endfor %}
    <tr style="background-color: #1a365d; color: white; font-weight: bold;">
        <td>合計</td>
        <td style="text-align: right;">¥{{ "{:,}".format(total) }}</td>
        <td>(税別)</td>
    </tr>
</table>
{% endif %}

<!-- リスク管理 -->
<h1>6. リスク管理</h1>
<table>
    <tr>
        <th>リスク</th>
        <th>影響度</th>
        <th>確率</th>
        <th>対策</th>
    </tr>
    {% for risk in risks %}
    <tr>
        <td>{{ risk.risk }}</td>
        <td>{{ risk.impact }}</td>
        <td>{{ risk.probability }}</td>
        <td>{{ risk.mitigation }}</td>
    </tr>
    {% endfor %}
</table>

{% if include_case_study %}
<!-- 導入事例 -->
<h1>7. 導入事例</h1>
{% for case in case_studies %}
<div class="highlight-box">
    <h2>{{ case.company }}（{{ case.industry }}）</h2>
    <p>{{ case.result }}</p>
</div>
{% endfor %}
{% endif %}

<!-- 署名 -->
<div class="signature">
    <p>上記の通り、ご提案申し上げます。</p>
    <div class="signature-line">
        {{ company_name }}<br>
        代表取締役<br><br>
        {{ approval_date }}
    </div>
</div>

</body>
</html>
'''

# HTMLをPDFに変換（Playwright / dataはJSONで上書き可能）
import asyncio
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


async def generate_proposal_pdf(output_path: str, render_data: dict):
    """提案書PDFを生成"""
    from jinja2 import Template

    # Jinja2でテンプレートをレンダリング
    template = Template(TEMPLATE_CONTENT)
    html_content = template.render(**render_data)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content)
        await page.wait_for_timeout(2000)
        await page.pdf(
            path=str(output),
            format="A4",
            print_background=True,
            margin={"top": "20mm", "right": "20mm", "bottom": "20mm", "left": "20mm"},
        )
        await browser.close()

    print(f"Created: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate proposal PDF from Jinja2 HTML (Playwright)")
    parser.add_argument("--output", default=str(Path("output/advanced/04_proposal_template.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    overrides = _load_data(args)
    merged = {**data, **(overrides or {})}
    asyncio.run(generate_proposal_pdf(args.output, merged))


if __name__ == "__main__":
    main()
