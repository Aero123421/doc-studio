#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XlsxWriterによる高度なExcelレポート生成
- 条件付き書式
- チャート埋め込み
- データ検証
- プロフェッショナルダッシュボード
"""

import argparse
import json
from pathlib import Path

import xlsxwriter
import datetime
import random


def _load_data(args: argparse.Namespace) -> dict:
    if args.data and args.data_file:
        raise SystemExit("Use either --data or --data-file (not both)")

    if args.data_file:
        p = Path(args.data_file)
        return json.loads(p.read_text(encoding="utf-8"))

    if args.data:
        return json.loads(args.data)

    return {}


def create_advanced_excel(output_path: str, _data: dict | None = None):
    """高度なExcelレポートを作成"""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    workbook = xlsxwriter.Workbook(str(out))

    # フォーマット定義
    formats = {}

    # タイトルフォーマット
    formats['title'] = workbook.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': '#1a365d',
        'font_name': 'Calibri',
        'valign': 'vcenter'
    })

    # ヘッダーフォーマット
    formats['header'] = workbook.add_format({
        'bold': True,
        'font_size': 11,
        'font_color': 'white',
        'bg_color': '#1a365d',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })

    # サブヘッダー
    formats['subheader'] = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'font_color': '#2c5282',
        'bg_color': '#e2e8f0',
        'border': 1,
        'align': 'left',
        'valign': 'vcenter'
    })

    # データセル
    formats['cell'] = workbook.add_format({
        'font_size': 10,
        'border': 1,
        'align': 'left',
        'valign': 'vcenter'
    })

    formats['cell_center'] = workbook.add_format({
        'font_size': 10,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })

    formats['cell_number'] = workbook.add_format({
        'font_size': 10,
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '#,##0'
    })

    formats['cell_currency'] = workbook.add_format({
        'font_size': 10,
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '¥#,##0'
    })

    formats['cell_percent'] = workbook.add_format({
        'font_size': 10,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '0.0%'
    })

    # 日付フォーマット
    formats['cell_date'] = workbook.add_format({
        'font_size': 10,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'num_format': 'yyyy-mm-dd'
    })

    # KPIカード用
    formats['kpi_value'] = workbook.add_format({
        'bold': True,
        'font_size': 24,
        'font_color': '#1a365d',
        'align': 'center',
        'valign': 'vcenter'
    })

    formats['kpi_label'] = workbook.add_format({
        'font_size': 10,
        'font_color': '#718096',
        'align': 'center',
        'valign': 'vcenter'
    })

    formats['kpi_change_positive'] = workbook.add_format({
        'font_size': 11,
        'font_color': '#48bb78',
        'align': 'center',
        'valign': 'vcenter'
    })

    formats['kpi_change_negative'] = workbook.add_format({
        'font_size': 11,
        'font_color': '#e53e3e',
        'align': 'center',
        'valign': 'vcenter'
    })

    # ハイライト
    formats['highlight'] = workbook.add_format({
        'bold': True,
        'bg_color': '#fef3c7',
        'border': 1
    })

    # ===== シート1: ダッシュボード =====
    dashboard = workbook.add_worksheet('Dashboard')
    dashboard.set_tab_color('#1a365d')

    # タイトル
    dashboard.merge_range('A1:G1', 'Business Intelligence Dashboard - Q4 2025', formats['title'])
    dashboard.set_row(0, 40)

    # 日付
    dashboard.write('A2', f'Report Date: {datetime.date.today().strftime("%Y-%m-%d")}', formats['cell'])

    # KPIセクション
    dashboard.write('A4', 'Key Performance Indicators', formats['subheader'])
    dashboard.merge_range('A4:G4', '', formats['subheader'])

    kpis = [
        ('Revenue', 1250000000, 0.23, 'currency'),
        ('Profit Margin', 0.185, 0.023, 'percent'),
        ('Customers', 2450, 0.12, 'number'),
        ('NPS Score', 94, 0.05, 'number'),
    ]

    kpi_cols = ['B', 'D', 'F']
    for i, (label, value, change, fmt) in enumerate(kpis):
        col = chr(ord('A') + i * 2)
        row = 6

        # KPIラベル
        dashboard.write(f'{col}{row}', label, formats['kpi_label'])

        # KPI値
        if fmt == 'currency':
            display_value = f'¥{value/100000000:.1f}B'
            dashboard.write(f'{col}{row+1}', display_value, formats['kpi_value'])
        elif fmt == 'percent':
            display_value = f'{value*100:.1f}%'
            dashboard.write(f'{col}{row+1}', display_value, formats['kpi_value'])
        else:
            dashboard.write(f'{col}{row+1}', value, formats['kpi_value'])

        # 変化率
        change_fmt = formats['kpi_change_positive'] if change > 0 else formats['kpi_change_negative']
        change_symbol = '+' if change > 0 else ''
        if fmt == 'percent' or fmt == 'number':
            dashboard.write(f'{col}{row+2}', f'{change_symbol}{change*100:.1f}%', change_fmt)
        else:
            dashboard.write(f'{col}{row+2}', f'{change_symbol}{change*100:.0f}%', change_fmt)

    # チャート埋め込み領域
    dashboard.write('A10', 'Revenue Trend', formats['subheader'])
    dashboard.merge_range('A10:G10', '', formats['subheader'])

    # ===== シート2: 売上データ =====
    sales_sheet = workbook.add_worksheet('Sales Data')
    sales_sheet.set_tab_color('#2c5282')

    # ヘッダー
    headers = ['Quarter', 'Product', 'Region', 'Sales Amount', 'Units Sold', 'Growth %', 'Status']
    for col, header in enumerate(headers):
        sales_sheet.write(0, col, header, formats['header'])

    # データ生成
    quarters = ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025']
    products = ['Product A', 'Product B', 'Product C', 'Product D']
    regions = ['North', 'South', 'East', 'West']

    row = 1
    data_rows = []
    for quarter in quarters:
        for product in products:
            for region in regions:
                sales = random.randint(500000, 2000000)
                units = random.randint(100, 500)
                growth = random.uniform(-0.1, 0.5)

                sales_sheet.write(row, 0, quarter, formats['cell_center'])
                sales_sheet.write(row, 1, product, formats['cell'])
                sales_sheet.write(row, 2, region, formats['cell_center'])
                sales_sheet.write(row, 3, sales, formats['cell_currency'])
                sales_sheet.write(row, 4, units, formats['cell_number'])
                sales_sheet.write(row, 5, growth, formats['cell_percent'])

                # ステータス条件付き
                if growth > 0.2:
                    status = 'Excellent'
                elif growth > 0:
                    status = 'Good'
                elif growth > -0.05:
                    status = 'Warning'
                else:
                    status = 'Critical'

                sales_sheet.write(row, 6, status, formats['cell_center'])
                data_rows.append(row)
                row += 1

    # 列幅調整
    sales_sheet.set_column('A:A', 12)
    sales_sheet.set_column('B:B', 15)
    sales_sheet.set_column('C:C', 12)
    sales_sheet.set_column('D:D', 15)
    sales_sheet.set_column('E:E', 12)
    sales_sheet.set_column('F:F', 12)
    sales_sheet.set_column('G:G', 12)

    # 条件付き書式
    # Growth % に基づいて色付け
    sales_sheet.conditional_format(f'F2:F{row}', {
        'type': 'cell',
        'criteria': '>',
        'value': 0.2,
        'format': workbook.add_format({'bg_color': '#c6efce', 'font_color': '#006100'})
    })
    sales_sheet.conditional_format(f'F2:F{row}', {
        'type': 'cell',
        'criteria': '<',
        'value': 0,
        'format': workbook.add_format({'bg_color': '#ffc7ce', 'font_color': '#9c0006'})
    })

    # Status列のアイコン付き条件付き書式
    sales_sheet.conditional_format(f'G2:G{row}', {
        'type': 'text',
        'criteria': 'containing',
        'value': 'Excellent',
        'format': workbook.add_format({'bg_color': '#c6efce', 'font_color': '#006100', 'bold': True})
    })
    sales_sheet.conditional_format(f'G2:G{row}', {
        'type': 'text',
        'criteria': 'containing',
        'value': 'Critical',
        'format': workbook.add_format({'bg_color': '#ffc7ce', 'font_color': '#9c0006', 'bold': True})
    })

    # データ検証
    sales_sheet.data_validation('B2:B100', {
        'validate': 'list',
        'source': products,
        'input_title': 'Select Product',
        'input_message': 'Please select from the list'
    })

    # 集計行
    summary_row = row + 1
    sales_sheet.write(summary_row, 0, 'TOTAL', formats['subheader'])
    sales_sheet.write_formula(summary_row, 3, f'=SUM(D2:D{row})', formats['cell_currency'])
    sales_sheet.write_formula(summary_row, 4, f'=SUM(E2:E{row})', formats['cell_number'])
    sales_sheet.write_formula(summary_row, 5, f'=AVERAGE(F2:F{row})', formats['cell_percent'])

    # ===== シート3: チャート分析 =====
    chart_sheet = workbook.add_worksheet('Charts')
    chart_sheet.set_tab_color('#c9a227')

    # チャート用データ
    chart_data = [
        ['Quarter', 'Revenue', 'Profit', 'Target'],
        ['Q1', 2800, 420, 2500],
        ['Q2', 3100, 520, 3000],
        ['Q3', 3300, 610, 3200],
        ['Q4', 3300, 640, 3400],
    ]

    for row_idx, row_data in enumerate(chart_data):
        for col_idx, value in enumerate(row_data):
            if row_idx == 0:
                chart_sheet.write(row_idx, col_idx, value, formats['header'])
            else:
                fmt = formats['cell_number'] if col_idx > 0 else formats['cell_center']
                chart_sheet.write(row_idx, col_idx, value, fmt)

    # 売上チャート
    chart1 = workbook.add_chart({'type': 'column'})
    chart1.add_series({
        'name': '=Charts!$B$1',
        'categories': '=Charts!$A$2:$A$5',
        'values': '=Charts!$B$2:$B$5',
        'fill': {'color': '#1a365d'},
        'data_labels': {'value': True}
    })
    chart1.add_series({
        'name': '=Charts!$D$1',
        'categories': '=Charts!$A$2:$A$5',
        'values': '=Charts!$D$2:$D$5',
        'fill': {'color': '#e2e8f0'},
        'border': {'color': '#c9a227', 'width': 2, 'dash_type': 'dash'}
    })
    chart1.set_title({'name': 'Revenue vs Target', 'font': {'size': 14, 'bold': True}})
    chart1.set_x_axis({'name': 'Quarter'})
    chart1.set_y_axis({'name': 'Amount (M¥)'})
    chart1.set_size({'width': 576, 'height': 320})
    chart_sheet.insert_chart('F2', chart1)

    # 利益率チャート
    chart2 = workbook.add_chart({'type': 'line'})
    chart2.add_series({
        'name': '=Charts!$C$1',
        'categories': '=Charts!$A$2:$A$5',
        'values': '=Charts!$C$2:$C$5',
        'line': {'color': '#c9a227', 'width': 3},
        'marker': {'type': 'circle', 'size': 8, 'fill': {'color': '#c9a227'}}
    })
    chart2.set_title({'name': 'Profit Trend', 'font': {'size': 14, 'bold': True}})
    chart2.set_x_axis({'name': 'Quarter'})
    chart2.set_y_axis({'name': 'Profit (M¥)'})
    chart2.set_size({'width': 576, 'height': 320})
    chart_sheet.insert_chart('F20', chart2)

    # ===== シート4: ピボット風サマリー =====
    pivot_sheet = workbook.add_worksheet('Pivot Summary')
    pivot_sheet.set_tab_color('#48bb78')

    # クロス集計風データ
    pivot_sheet.write('A1', 'Sales by Region & Product', formats['title'])
    pivot_sheet.merge_range('A1:E1', '', formats['title'])

    # 行ラベル
    pivot_sheet.write('A3', 'Region', formats['header'])
    for i, product in enumerate(products):
        pivot_sheet.write(2, i+1, product, formats['header'])
    pivot_sheet.write(2, 5, 'Total', formats['header'])

    # データ
    for i, region in enumerate(regions):
        row = 3 + i
        pivot_sheet.write(row, 0, region, formats['subheader'])

        for j, product in enumerate(products):
            # SUMIFS風の計算式
            formula = f"=SUMIFS('Sales Data'!$D:$D,'Sales Data'!$C:$C,$A{row+1},'Sales Data'!$B:$B,B$3)"
            pivot_sheet.write_formula(row, j+1, formula, formats['cell_currency'])

        # 行合計
        pivot_sheet.write_formula(row, 5, f'=SUM(B{row+1}:E{row+1})', formats['cell_currency'])

    # 列合計
    pivot_sheet.write(7, 0, 'Total', formats['header'])
    for col in range(1, 6):
        col_letter = chr(ord('A') + col)
        pivot_sheet.write_formula(7, col, f'=SUM({col_letter}4:{col_letter}7)', formats['cell_currency'])

    # ヒートマップ条件付き書式
    pivot_sheet.conditional_format('B4:E7', {
        'type': '3_color_scale',
        'min_color': '#ffffff',
        'mid_color': '#fff2cc',
        'max_color': '#c9a227'
    })

    # 列幅調整
    for col in range(6):
        pivot_sheet.set_column(col, col, 18)

    workbook.close()
    print(f"Created: {out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate advanced Excel dashboard (XlsxWriter)")
    parser.add_argument("--output", default=str(Path("output/advanced/06_excel_dashboard.xlsx")))
    parser.add_argument("--data", help="Inline JSON string (optional)")
    parser.add_argument("--data-file", help="JSON file path (optional)")
    args = parser.parse_args()

    data = _load_data(args)
    create_advanced_excel(args.output, data)
