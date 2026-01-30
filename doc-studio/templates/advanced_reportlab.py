#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ReportLabによる高度なPDF生成
- 完全プログラマティック制御
- 複雑なレイアウト、グラデーション、チャート
- 印刷品質の最高レベル
"""

import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, Frame, PageTemplate, NextPageTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np


def _load_data(args: argparse.Namespace) -> dict:
    if args.data and args.data_file:
        raise SystemExit("Use either --data or --data-file (not both)")

    if args.data_file:
        p = Path(args.data_file)
        return json.loads(p.read_text(encoding="utf-8"))

    if args.data:
        return json.loads(args.data)

    return {}

class AdvancedReport:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        """カスタムスタイル定義"""
        # タイトルスタイル
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=colors.HexColor('#1a5f7a'),
            fontName='Helvetica-Bold'
        ))

        # サブタイトル
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#666666')
        ))

        # ヘッダー1
        self.styles.add(ParagraphStyle(
            name='CustomH1',
            fontSize=18,
            leading=22,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#1a5f7a'),
            fontName='Helvetica-Bold',
            borderColor=colors.HexColor('#1a5f7a'),
            borderWidth=2,
            borderPadding=5
        ))

        # ヘッダー2
        self.styles.add(ParagraphStyle(
            name='CustomH2',
            fontSize=14,
            leading=18,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor('#159895'),
            fontName='Helvetica-Bold'
        ))

        # 本文
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            firstLineIndent=20
        ))

        # キャプション
        self.styles.add(ParagraphStyle(
            name='Caption',
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666'),
            spaceBefore=5
        ))

    def create_matplotlib_chart(self):
        """matplotlibで高品質チャートを作成"""
        fig, axes = plt.subplots(2, 2, figsize=(8, 6), dpi=150)
        fig.patch.set_facecolor('white')

        # サンプルデータ
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        sales = [120, 150, 180, 200, 240, 280]
        profit = [20, 30, 45, 50, 70, 90]

        # 1. 売上チャート
        ax1 = axes[0, 0]
        bars = ax1.bar(months, sales, color='#1a5f7a', alpha=0.8)
        ax1.set_title('Monthly Sales', fontweight='bold', fontsize=10)
        ax1.set_ylabel('Revenue (K$)')
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height}K', ha='center', va='bottom', fontsize=8)

        # 2. 利益チャート
        ax2 = axes[0, 1]
        ax2.plot(months, profit, marker='o', linewidth=2, color='#159895')
        ax2.fill_between(months, profit, alpha=0.3, color='#159895')
        ax2.set_title('Profit Trend', fontweight='bold', fontsize=10)
        ax2.set_ylabel('Profit (K$)')
        ax2.grid(True, alpha=0.3)

        # 3. 円グラフ
        ax3 = axes[1, 0]
        categories = ['Product A', 'Product B', 'Product C', 'Product D']
        values = [35, 25, 25, 15]
        colors_pie = ['#1a5f7a', '#159895', '#57c5b6', '#e8f6f3']
        wedges, texts, autotexts = ax3.pie(values, labels=categories, autopct='%1.0f%%',
                                            colors=colors_pie, startangle=90)
        ax3.set_title('Sales by Product', fontweight='bold', fontsize=10)

        # 4. ヒートマップ
        ax4 = axes[1, 1]
        data = np.random.rand(5, 5)
        im = ax4.imshow(data, cmap='YlGnBu', aspect='auto')
        ax4.set_title('Performance Heatmap', fontweight='bold', fontsize=10)
        ax4.set_xticks(range(5))
        ax4.set_yticks(range(5))
        plt.colorbar(im, ax=ax4, shrink=0.8)

        plt.tight_layout()

        # BytesIOに保存
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        plt.close()

        return img_buffer

    def add_complex_table(self):
        """複雑なテーブルレイアウト"""
        data = [
            ['部門', 'Q1', 'Q2', 'Q3', 'Q4', '合計', '達成率'],
            ['営業部', '¥50M', '¥65M', '¥72M', '¥85M', '¥272M', '109%'],
            ['開発部', '¥30M', '¥35M', '¥40M', '¥45M', '¥150M', '115%'],
            ['マーケ部', '¥20M', '¥28M', '¥32M', '¥38M', '¥118M', '118%'],
            ['総務部', '¥10M', '¥12M', '¥11M', '¥13M', '¥46M', '92%'],
        ]

        table = Table(data, colWidths=[3*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2.5*cm, 1.5*cm])

        style = TableStyle([
            # ヘッダー
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5f7a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # ボディ
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),

            # 合計行
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f6f3')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),

            # 罫線
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1a5f7a')),

            # パディング
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),

            # 達成率の色分け
            ('TEXTCOLOR', (6, 1), (6, 1), colors.green),
            ('TEXTCOLOR', (6, 2), (6, 2), colors.green),
            ('TEXTCOLOR', (6, 3), (6, 3), colors.green),
            ('TEXTCOLOR', (6, 4), (6, 4), colors.red),
        ])

        table.setStyle(style)
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))

    def add_gradient_box(self, title, content):
        """グラデーション風のボックス"""
        # タイトル
        self.story.append(Paragraph(f"<b>{title}</b>", self.styles['CustomH2']))

        # 内容をテーブルで囲む（背景色で表現）
        data = [[content]]
        table = Table(data, colWidths=[16*cm])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#1a5f7a')),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ])
        table.setStyle(style)
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))

    def add_two_column_layout(self, left_content, right_content):
        """2カラムレイアウト"""
        data = [[left_content, right_content]]
        table = Table(data, colWidths=[8*cm, 8*cm], hAlign='LEFT')
        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ])
        table.setStyle(style)
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))

    def generate(self):
        """レポート生成"""
        # タイトルページ
        self.story.append(Spacer(1, 5*cm))
        self.story.append(Paragraph("Business Intelligence Report", self.styles['CustomTitle']))
        self.story.append(Paragraph("Q4 2025 Financial Analysis & Strategic Outlook", self.styles['CustomSubtitle']))
        self.story.append(Spacer(1, 2*cm))

        # 区切り線
        line_data = [['']]
        line_table = Table(line_data, colWidths=[16*cm], rowHeights=[2])
        line_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a5f7a')),
        ]))
        self.story.append(line_table)
        self.story.append(Spacer(1, 1*cm))

        # メタ情報
        meta_text = """
        <para alignment="center">
        <font size="10" color="#666666">
        Prepared by: Strategic Planning Department<br/>
        Date: January 2026 | Version: 2.0 | Classification: Internal Use
        </font>
        </para>
        """
        self.story.append(Paragraph(meta_text, self.styles['Normal']))

        self.story.append(PageBreak())

        # エグゼクティブサマリー
        self.story.append(Paragraph("Executive Summary", self.styles['CustomH1']))
        summary_text = """
        本レポートでは、2025年度第4四半期の財務パフォーマンスと戦略的イニシアチブの
        包括的な分析を提供します。主要なハイライトとして、売上高の前年比18%増、
        営業利益率の改善、および新規市場参入の成功が挙げられます。
        """
        self.story.append(Paragraph(summary_text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.5*cm))

        # グラデーションボックス
        self.add_gradient_box(
            "Key Highlights",
            "• Revenue growth: <b>+18% YoY</b><br/>"
            "• Operating margin: <b>Improved by 2.3pp</b><br/>"
            "• New market penetration: <b>3 regions</b><br/>"
            "• Customer satisfaction: <b>94% (+5pp)</b>"
        )

        self.story.append(PageBreak())

        # チャートセクション
        self.story.append(Paragraph("Performance Analytics", self.styles['CustomH1']))

        # matplotlibチャート
        chart_buffer = self.create_matplotlib_chart()
        img = Image(chart_buffer, width=16*cm, height=12*cm)
        self.story.append(img)
        self.story.append(Paragraph("Figure 1: Comprehensive Performance Dashboard", self.styles['Caption']))
        self.story.append(Spacer(1, 0.5*cm))

        self.story.append(PageBreak())

        # テーブルセクション
        self.story.append(Paragraph("Department Performance", self.styles['CustomH1']))
        self.add_complex_table()

        # 2カラムレイアウト
        self.story.append(Paragraph("Strategic Initiatives", self.styles['CustomH1']))

        left = """
        <b>Digital Transformation</b><br/><br/>
        クラウドインフラストラクチャの完全移行を完了し、
        運用効率が40%向上しました。AIを活用した予測分析システムの
        導入により、需要予測の精度が大幅に改善されました。
        """

        right = """
        <b>Sustainability Goals</b><br/><br/>
        2030年までにカーボンニュートラルを達成するための
        ロードマップを策定。現在、再生可能エネルギーの比率を
        65%まで引き上げることができました。
        """

        self.add_two_column_layout(
            Paragraph(left, self.styles['CustomBody']),
            Paragraph(right, self.styles['CustomBody'])
        )

        # PDF生成
        self.doc.build(self.story)
        print(f"Created: {self.filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate advanced PDF (ReportLab)")
    parser.add_argument("--output", default=str(Path("output/advanced/01_reportlab_advanced.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    _ = _load_data(args)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    report = AdvancedReport(str(out))
    report.generate()
