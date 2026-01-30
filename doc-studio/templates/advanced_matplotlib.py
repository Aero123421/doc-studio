#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
matplotlib + seabornによるデータ可視化レポート
- 出版品質のチャート
- 複数の可視化手法
- PDF出力統合
"""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import matplotlib.patches as mpatches

# 日本語フォント設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans JP', 'Hiragino Sans', 'Meiryo']
plt.rcParams['axes.unicode_minus'] = False

# スタイル設定
sns.set_style("whitegrid")
sns.set_palette("husl")

def _load_data(args: argparse.Namespace) -> dict:
    if args.data and args.data_file:
        raise SystemExit("Use either --data or --data-file (not both)")

    if args.data_file:
        p = Path(args.data_file)
        return json.loads(p.read_text(encoding="utf-8"))

    if args.data:
        return json.loads(args.data)

    return {}


def create_advanced_charts(output_path: str, _data: dict | None = None):
    """高度なチャート集を作成"""

    # PDFファイルを作成
    pdf_path = str(Path(output_path))
    Path(pdf_path).parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(pdf_path) as pdf:

        # ===== ページ1: カバー =====
        fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
        fig.patch.set_facecolor('#1a1a2e')

        ax = fig.add_subplot(111)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        ax.set_facecolor('#1a1a2e')

        # タイトル
        ax.text(5, 6, 'Data Visualization Report', fontsize=32, ha='center',
                color='white', fontweight='bold')
        ax.text(5, 4.5, 'Advanced Analytics Dashboard', fontsize=16, ha='center',
                color='#c9a227')
        ax.text(5, 3, '2026 Q1 Business Intelligence', fontsize=12, ha='center',
                color='#888')

        # 装飾
        circle = Circle((1, 8), 0.5, color='#c9a227', alpha=0.3)
        ax.add_patch(circle)
        circle2 = Circle((9, 2), 0.8, color='#533483', alpha=0.3)
        ax.add_patch(circle2)

        pdf.savefig(fig, facecolor='#1a1a2e', bbox_inches='tight')
        plt.close()

        # ===== ページ2: サマリーダッシュボード =====
        fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
        fig.suptitle('Executive Dashboard', fontsize=18, fontweight='bold', y=0.98)

        # KPIカード風の表示
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

        metrics = [
            ('Revenue', '$12.5M', '+23%', '#1a5f7a'),
            ('Profit', '$2.3M', '+18%', '#28a745'),
            ('Customers', '15.2K', '+15%', '#dc3545'),
            ('Orders', '45.8K', '+28%', '#fd7e14'),
            ('Satisfaction', '94%', '+5pp', '#6f42c1'),
            ('Efficiency', '87%', '+12pp', '#20c997'),
        ]

        for i, (name, value, change, color) in enumerate(metrics):
            ax = fig.add_subplot(gs[i//3, i%3])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')

            # 背景ボックス
            box = FancyBboxPatch((0.05, 0.1), 0.9, 0.8,
                                  boxstyle="round,pad=0.02",
                                  facecolor=color, alpha=0.1,
                                  edgecolor=color, linewidth=2)
            ax.add_patch(box)

            ax.text(0.5, 0.7, name, ha='center', va='center', fontsize=10, color='#666')
            ax.text(0.5, 0.45, value, ha='center', va='center', fontsize=20,
                   fontweight='bold', color=color)
            ax.text(0.5, 0.2, change, ha='center', va='center', fontsize=10,
                   color='green' if '+' in change else 'red')

        # 下部にミニチャート
        ax_chart = fig.add_subplot(gs[2, :])
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [10, 11, 11.5, 12, 12.3, 12.5]
        ax_chart.plot(months, revenue, marker='o', linewidth=3, markersize=8,
                     color='#1a5f7a', label='Revenue')
        ax_chart.fill_between(months, revenue, alpha=0.3, color='#1a5f7a')
        ax_chart.set_title('6-Month Revenue Trend', fontsize=12, pad=10)
        ax_chart.set_ylabel('Million $')
        ax_chart.grid(True, alpha=0.3)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # ===== ページ3: 複合チャート =====
        fig, axes = plt.subplots(2, 2, figsize=(11.69, 8.27), dpi=150)
        fig.suptitle('Multi-Dimensional Analysis', fontsize=16, fontweight='bold')

        # 1. 売上・利益のトレンド
        ax1 = axes[0, 0]
        x = np.arange(1, 13)
        sales = [8.5, 9.0, 9.2, 10.1, 10.5, 11.0, 11.3, 11.8, 12.0, 12.2, 12.4, 12.5]
        profit = [1.2, 1.4, 1.5, 1.8, 1.9, 2.0, 2.1, 2.2, 2.25, 2.3, 2.35, 2.4]

        ax1_twin = ax1.twinx()
        bars = ax1.bar(x, sales, alpha=0.7, color='#1a5f7a', label='Sales')
        line = ax1_twin.plot(x, profit, color='#c9a227', marker='o', linewidth=2, label='Profit')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Sales ($M)', color='#1a5f7a')
        ax1_twin.set_ylabel('Profit ($M)', color='#c9a227')
        ax1.set_title('Sales vs Profit Trend')

        # 2. 部門別比較（グループドバー）
        ax2 = axes[0, 1]
        departments = ['Sales', 'Marketing', 'Dev', 'Support', 'HR']
        q1 = [85, 65, 90, 70, 55]
        q2 = [88, 72, 92, 75, 60]
        q3 = [92, 78, 95, 80, 62]

        x = np.arange(len(departments))
        width = 0.25

        ax2.bar(x - width, q1, width, label='Q1', color='#e8f4f8')
        ax2.bar(x, q2, width, label='Q2', color='#7fcdbb')
        ax2.bar(x + width, q3, width, label='Q3', color='#2c7fb8')
        ax2.set_ylabel('Score')
        ax2.set_title('Department Performance by Quarter')
        ax2.set_xticks(x)
        ax2.set_xticklabels(departments)
        ax2.legend()

        # 3. ヒートマップ
        ax3 = axes[1, 0]
        correlation_data = np.random.rand(8, 8)
        correlation_data = (correlation_data + correlation_data.T) / 2
        np.fill_diagonal(correlation_data, 1)

        sns.heatmap(correlation_data, annot=True, fmt='.2f', cmap='RdYlBu_r',
                   center=0.5, square=True, ax=ax3, cbar_kws={'shrink': 0.8})
        ax3.set_title('Correlation Matrix')

        # 4. 散布図＋回帰線
        ax4 = axes[1, 1]
        np.random.seed(42)
        x_scatter = np.random.randn(100) * 10 + 50
        y_scatter = 0.8 * x_scatter + np.random.randn(100) * 5 + 20

        sns.regplot(x=x_scatter, y=y_scatter, ax=ax4, color='#1a5f7a',
                   scatter_kws={'alpha': 0.5}, line_kws={'color': '#c9a227'})
        ax4.set_xlabel('Marketing Spend ($K)')
        ax4.set_ylabel('Revenue ($K)')
        ax4.set_title('Marketing ROI Analysis')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # ===== ページ4: 高度な可視化 =====
        fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

        # 1. ドーナツチャート
        ax1 = fig.add_subplot(gs[0, 0])
        sizes = [35, 25, 20, 15, 5]
        labels = ['Product A', 'Product B', 'Product C', 'Product D', 'Others']
        colors_donut = plt.cm.Set3(np.linspace(0, 1, len(sizes)))
        wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
                                          colors=colors_donut, startangle=90,
                                          wedgeprops=dict(width=0.5))
        ax1.set_title('Product Mix')

        # 2. ボックスプロット
        ax2 = fig.add_subplot(gs[0, 1])
        data_box = [np.random.normal(100, 20, 100) for _ in range(5)]
        bp = ax2.boxplot(data_box, patch_artist=True)
        for patch, color in zip(bp['boxes'], plt.cm.Pastel1(np.linspace(0, 1, 5))):
            patch.set_facecolor(color)
        ax2.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])
        ax2.set_title('Daily Performance Distribution')

        # 3. バイオリンプロット
        ax3 = fig.add_subplot(gs[0, 2])
        data_violin = [np.random.gamma(2, 40, 200) + i*10 for i in range(4)]
        parts = ax3.violinplot(data_violin, showmeans=True, showmedians=True)
        for pc, color in zip(parts['bodies'], plt.cm.Set2(np.linspace(0, 1, 4))):
            pc.set_facecolor(color)
        ax3.set_xticks([1, 2, 3, 4])
        ax3.set_xticklabels(['A', 'B', 'C', 'D'])
        ax3.set_title('Distribution by Category')

        # 4. 面グラフ
        ax4 = fig.add_subplot(gs[1, :2])
        x_area = np.arange(12)
        y1 = np.cumsum(np.random.randn(12)) + 50
        y2 = np.cumsum(np.random.randn(12)) + 45
        y3 = np.cumsum(np.random.randn(12)) + 40

        ax4.fill_between(x_area, y1, alpha=0.5, label='Team A', color='#1a5f7a')
        ax4.fill_between(x_area, y2, alpha=0.5, label='Team B', color='#c9a227')
        ax4.fill_between(x_area, y3, alpha=0.5, label='Team C', color='#dc3545')
        ax4.set_xticks(x_area)
        ax4.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax4.set_title('Cumulative Performance by Team')
        ax4.legend(loc='upper left')

        # 5. 水平バーチャート
        ax5 = fig.add_subplot(gs[1, 2])
        categories = ['Feature A', 'Feature B', 'Feature C', 'Feature D', 'Feature E']
        values = [92, 88, 85, 78, 72]
        colors_bar = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(values)))

        bars = ax5.barh(categories, values, color=colors_bar)
        ax5.set_xlim(0, 100)
        for i, (bar, val) in enumerate(zip(bars, values)):
            ax5.text(val + 1, i, f'{val}%', va='center', fontsize=9)
        ax5.set_title('Feature Satisfaction')

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # ===== ページ5: 3Dチャート =====
        fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
        fig.suptitle('3D Visualization', fontsize=16, fontweight='bold')

        # 3Dバーチャート
        ax = fig.add_subplot(111, projection='3d')

        _x = np.arange(4)
        _y = np.arange(5)
        _xx, _yy = np.meshgrid(_x, _y)
        x, y = _xx.ravel(), _yy.ravel()

        top = np.random.randint(10, 100, size=len(x))
        bottom = np.zeros_like(top)
        width = depth = 0.5

        colors_3d = plt.cm.viridis(top / 100)
        ax.bar3d(x, y, bottom, width, depth, top, shade=True, color=colors_3d)

        ax.set_xlabel('Product')
        ax.set_ylabel('Region')
        ax.set_zlabel('Sales')
        ax.set_title('Sales by Product and Region', pad=20)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    print(f"Created: {pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate data report PDF (matplotlib/seaborn)")
    parser.add_argument("--output", default=str(Path("output/advanced/03_matplotlib_datareport.pdf")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    create_advanced_charts(args.output, data)
