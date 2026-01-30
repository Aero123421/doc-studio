#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FPDF2による現代的なPDF生成
- 日本語完全対応
- フレックスボックス風レイアウト
- グラデーション、透明度対応
- 高速・軽量
"""

import argparse
import json
from pathlib import Path

from fpdf import FPDF
import os


def _load_data(args: argparse.Namespace) -> dict:
    if args.data and args.data_file:
        raise SystemExit("Use either --data or --data-file (not both)")

    if args.data_file:
        p = Path(args.data_file)
        return json.loads(p.read_text(encoding="utf-8"))

    if args.data:
        return json.loads(args.data)

    return {}

class ModernPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font('noto', '', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Annual Report 2026 | Page {self.page_no()}', 0, 0, 'R')
            self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('noto', '', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'{self.page_no()}', 0, 0, 'C')

    def add_gradient_rect(self, x, y, w, h, color1, color2, direction='vertical'):
        """グラデーション矩形を描画"""
        steps = 50
        if direction == 'vertical':
            step_h = h / steps
            for i in range(steps):
                ratio = i / steps
                r = int(color1[0] + (color2[0] - color1[0]) * ratio)
                g = int(color1[1] + (color2[1] - color1[1]) * ratio)
                b = int(color1[2] + (color2[2] - color1[2]) * ratio)
                self.set_fill_color(r, g, b)
                self.rect(x, y + i * step_h, w, step_h + 0.5, 'F')
        else:
            step_w = w / steps
            for i in range(steps):
                ratio = i / steps
                r = int(color1[0] + (color2[0] - color1[0]) * ratio)
                g = int(color1[1] + (color2[1] - color1[1]) * ratio)
                b = int(color1[2] + (color2[2] - color1[2]) * ratio)
                self.set_fill_color(r, g, b)
                self.rect(x + i * step_w, y, step_w + 0.5, h, 'F')

    def add_title_page(self):
        """表紙ページ"""
        self.add_page()

        # グラデーション背景
        self.add_gradient_rect(0, 0, 210, 100, (26, 32, 44), (45, 55, 72), 'vertical')
        self.add_gradient_rect(0, 100, 210, 197, (45, 55, 72), (255, 255, 255), 'vertical')

        # タイトル
        self.set_y(60)
        self.set_font('noto', 'B', 36)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, 'Annual Report', 0, 1, 'C')

        self.set_font('noto', '', 16)
        self.set_text_color(201, 162, 39)
        self.cell(0, 10, '2026 Fiscal Year', 0, 1, 'C')

        # サブタイトル
        self.set_y(130)
        self.set_font('noto', '', 14)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Comprehensive Business Review & Strategic Outlook', 0, 1, 'C')

        # メタ情報
        self.set_y(180)
        self.set_font('noto', '', 11)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, 'Prepared by: Corporate Strategy Division', 0, 1, 'C')
        self.cell(0, 8, 'Date: January 2026', 0, 1, 'C')
        self.cell(0, 8, 'Classification: Internal Use', 0, 1, 'C')

    def add_executive_summary(self):
        """エグゼクティブサマリー"""
        self.add_page()

        # 見出し
        self.set_font('noto', 'B', 20)
        self.set_text_color(26, 32, 44)
        self.cell(0, 15, 'Executive Summary', 0, 1, 'L')

        # ライン
        self.set_fill_color(201, 162, 39)
        self.rect(10, self.get_y(), 40, 2, 'F')
        self.ln(10)

        # 本文
        self.set_font('noto', '', 11)
        self.set_text_color(60, 60, 60)

        summary_text = """2025年度は、企業変革の重要な転換点となりました。デジタルトランスフォーメーションの完了とともに、新たな成長フェーズへの移行を成功させることができました。

市場環境の激しい変化の中、当社は革新的なソリューションと顧客中心のアプローチにより、競争優位性を確立しました。特にアジア太平洋地域での事業拡大は、予想を上回る成果を上げています。"""

        self.multi_cell(0, 8, summary_text)
        self.ln(10)

        # KPIカード風表示
        kpis = [
            ('¥12.5B', '総売上高', '+23%'),
            ('18.5%', '営業利益率', '+2.3pp'),
            ('2,450', '従業員数', '+12%'),
            ('94%', '顧客満足度', '+5pp'),
        ]

        card_width = 45
        card_height = 35
        start_x = 10
        y = self.get_y()

        for i, (value, label, change) in enumerate(kpis):
            x = start_x + i * (card_width + 5)

            # カード背景
            self.set_fill_color(248, 249, 250)
            self.rect(x, y, card_width, card_height, 'F')

            # 値
            self.set_xy(x, y + 5)
            self.set_font('noto', 'B', 16)
            self.set_text_color(26, 32, 44)
            self.cell(card_width, 10, value, 0, 1, 'C')

            # ラベル
            self.set_font('noto', '', 9)
            self.set_text_color(100, 100, 100)
            self.cell(card_width, 6, label, 0, 1, 'C')

            # 変化率
            self.set_font('noto', '', 9)
            self.set_text_color(40, 167, 69)
            self.cell(card_width, 6, change, 0, 1, 'C')

            # ボーダー
            self.set_draw_color(201, 162, 39)
            self.set_line_width(0.5)
            self.rect(x, y, card_width, card_height)

        self.ln(45)

    def add_financial_highlights(self):
        """財務ハイライト"""
        self.add_page()

        self.set_font('noto', 'B', 20)
        self.set_text_color(26, 32, 44)
        self.cell(0, 15, 'Financial Highlights', 0, 1, 'L')
        self.ln(5)

        # テーブルヘッダー
        col_widths = [35, 35, 35, 35, 35]
        headers = ['四半期', '売上高', '営業利益', '利益率', '前年比']

        # ヘッダー背景
        self.set_fill_color(26, 32, 44)
        self.set_text_color(255, 255, 255)
        self.set_font('noto', 'B', 10)
        self.set_draw_color(26, 32, 44)

        for i, header in enumerate(headers):
            self.cell(col_widths[i], 12, header, 1, 0, 'C', True)
        self.ln()

        # データ
        data = [
            ['Q1 2025', '¥2.8B', '¥420M', '15.0%', '+8%'],
            ['Q2 2025', '¥3.1B', '¥520M', '16.8%', '+12%'],
            ['Q3 2025', '¥3.3B', '¥610M', '18.5%', '+18%'],
            ['Q4 2025', '¥3.3B', '¥640M', '19.4%', '+22%'],
        ]

        self.set_font('noto', '', 10)

        for row_idx, row in enumerate(data):
            # 交互の背景色
            if row_idx % 2 == 0:
                self.set_fill_color(248, 249, 250)
            else:
                self.set_fill_color(255, 255, 255)

            self.set_text_color(60, 60, 60)

            for i, cell in enumerate(row):
                align = 'R' if i > 0 else 'L'
                self.cell(col_widths[i], 10, cell, 1, 0, align, True)
            self.ln()

        self.ln(15)

        # ビジネスセグメント
        self.set_font('noto', 'B', 14)
        self.set_text_color(26, 32, 44)
        self.cell(0, 10, 'Segment Performance', 0, 1, 'L')
        self.ln(5)

        segments = [
            ('Enterprise Solutions', '45%', '¥5.6B'),
            ('Cloud Services', '30%', '¥3.8B'),
            ('Consulting', '15%', '¥1.9B'),
            ('Support Services', '10%', '¥1.2B'),
        ]

        for name, percentage, revenue in segments:
            # プログレスバー風
            bar_width = 120
            fill_width = bar_width * int(percentage[:-1]) // 100

            # ラベル
            self.set_font('noto', 'B', 10)
            self.set_text_color(60, 60, 60)
            self.cell(60, 8, name, 0, 0, 'L')

            # バー背景
            self.set_fill_color(230, 230, 230)
            self.rect(70, self.get_y() + 2, bar_width, 6, 'F')

            # バー塗り
            self.set_fill_color(26, 32, 44)
            self.rect(70, self.get_y() + 2, fill_width, 6, 'F')

            # 値
            self.set_x(195)
            self.set_font('noto', '', 10)
            self.cell(0, 8, f'{revenue} ({percentage})', 0, 1, 'R')

            self.ln(5)

    def add_strategic_initiatives(self):
        """戦略イニシアチブ"""
        self.add_page()

        self.set_font('noto', 'B', 20)
        self.set_text_color(26, 32, 44)
        self.cell(0, 15, 'Strategic Initiatives', 0, 1, 'L')
        self.ln(5)

        initiatives = [
            {
                'title': 'デジタルトランスフォーメーション',
                'status': '完了',
                'progress': 100,
                'description': '全業務システムのクラウド移行とAI活用による自動化を完了。運用効率が40%向上。'
            },
            {
                'title': 'アジア太平洋地域展開',
                'status': '進行中',
                'progress': 75,
                'description': 'シンガポール・バンコクに拠点を開設。現地パートナーとの提携を3件締結。'
            },
            {
                'title': 'カーボンニュートラル達成',
                'status': '進行中',
                'progress': 65,
                'description': '2030年までのカーボンニュートラルに向け、現在65%を再生可能エネルギーで賄う。'
            },
            {
                'title': '次世代人材育成',
                'status': '進行中',
                'progress': 80,
                'description': 'デジタル人材100名の採用と既存社員のスキルアッププログラムを実施。'
            },
        ]

        for init in initiatives:
            # タイトル
            self.set_font('noto', 'B', 12)
            self.set_text_color(26, 32, 44)
            self.cell(0, 8, init['title'], 0, 1, 'L')

            # ステータスバッジ
            if init['status'] == '完了':
                self.set_fill_color(40, 167, 69)
                self.set_text_color(255, 255, 255)
            else:
                self.set_fill_color(255, 193, 7)
                self.set_text_color(0, 0, 0)

            self.set_font('noto', 'B', 8)
            self.cell(20, 6, init['status'], 0, 0, 'C', True)

            # プログレス
            bar_width = 100
            fill_width = bar_width * init['progress'] // 100

            self.set_fill_color(230, 230, 230)
            self.rect(50, self.get_y() + 1, bar_width, 5, 'F')

            self.set_fill_color(201, 162, 39)
            self.rect(50, self.get_y() + 1, fill_width, 5, 'F')

            self.set_x(155)
            self.set_font('noto', '', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 6, f"{init['progress']}%", 0, 1, 'L')

            # 説明
            self.set_font('noto', '', 10)
            self.set_text_color(80, 80, 80)
            self.multi_cell(0, 6, init['description'])
            self.ln(10)

def create_fpdf_report(output_path: str, _data: dict | None = None):
    """FPDF2で高度なPDFレポートを作成"""
    pdf = ModernPDF()

    # Noto Sansフォントを追加（システムにインストールされている前提）
    font_paths = [
        'C:/Windows/Fonts/NotoSansCJKjp-Regular.otf',
        'C:/Windows/Fonts/NotoSansJP-Regular.otf',
        'C:/Windows/Fonts/msgothic.ttc',
    ]

    font_found = False
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdf.add_font('noto', '', font_path, uni=True)
                pdf.add_font('noto', 'B', font_path, uni=True)
                font_found = True
                print(f'Font loaded: {font_path}')
                break
            except Exception as e:
                print(f'Font load error: {e}')
                continue

    if not font_found:
        print('Warning: Japanese font not found, using default')
        pdf.add_font('noto', '', 'C:/Windows/Fonts/arial.ttf', uni=True)
        pdf.add_font('noto', 'B', 'C:/Windows/Fonts/arialbd.ttf', uni=True)

    pdf.set_font('noto', '', 11)

    # ページ追加
    pdf.add_title_page()
    pdf.add_executive_summary()
    pdf.add_financial_highlights()
    pdf.add_strategic_initiatives()

    # 保存
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output))
    print(f"Created: {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate modern PDF (FPDF2)")
    parser.add_argument("--output", default=str(Path("output/advanced/05_fpdf2_modern.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    create_fpdf_report(args.output, data)
