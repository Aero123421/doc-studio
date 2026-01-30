#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphvizによる自動ダイアグラム生成
- システムアーキテクチャ図
- フローチャート
- ネットワーク図
- ER図
- 統合PDFレポート
"""

import argparse
import os
import shutil
from pathlib import Path

import graphviz
from graphviz import Digraph, Graph

DOT_AVAILABLE = shutil.which("dot") is not None


def _render_or_write(dot, output_base: Path) -> Path:
    output_base.parent.mkdir(parents=True, exist_ok=True)

    if DOT_AVAILABLE:
        rendered = dot.render(str(output_base), cleanup=True)
        return Path(rendered)

    # dotが無い場合はDOTソースを出力して終了（拡張子なしで既存サンプルと合わせる）
    output_base.write_text(dot.source, encoding="utf-8")
    return output_base

def create_system_architecture(output_dir: Path = Path("output/advanced")):
    """システムアーキテクチャ図"""
    dot = Digraph(comment='System Architecture', format='png')
    dot.attr(rankdir='TB', size='12,8', dpi='150')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    dot.attr('edge', fontname='Arial', fontsize='10')

    # カラーパレット
    colors = {
        'user': '#e3f2fd',
        'frontend': '#fff3e0',
        'gateway': '#fce4ec',
        'service': '#e8f5e9',
        'database': '#f3e5f5',
        'external': '#fff9c4',
    }

    # ノード定義
    dot.node('User', '👤 End User', fillcolor=colors['user'], shape='ellipse')
    dot.node('CDN', 'Cloud CDN\n(Azure Front Door)', fillcolor=colors['external'])
    dot.node('Web', 'Web Frontend\n(Next.js)', fillcolor=colors['frontend'])
    dot.node('Mobile', 'Mobile App\n(React Native)', fillcolor=colors['frontend'])
    dot.node('APIGW', 'API Gateway\n(Kong)', fillcolor=colors['gateway'])

    # マイクロサービス
    services = [
        ("Auth", "Auth Service\n(Node.js)", colors["service"]),
        ("UserSvc", "User Service\n(Go)", colors["service"]),
        ("Product", "Product Service\n(Java)", colors["service"]),
        ("Order", "Order Service\n(Python)", colors["service"]),
        ("Payment", "Payment Service\n(Go)", colors["service"]),
        ("Notification", "Notification\n(Node.js)", colors["service"]),
    ]

    for name, label, color in services:
        dot.node(name, label, fillcolor=color)

    # データベース
    databases = [
        ('UserDB', 'User DB\n(PostgreSQL)', colors['database']),
        ('ProductDB', 'Product DB\n(MongoDB)', colors['database']),
        ('OrderDB', 'Order DB\n(PostgreSQL)', colors['database']),
        ('Cache', 'Cache\n(Redis)', colors['database']),
        ('Queue', 'Message Queue\n(RabbitMQ)', colors['database']),
    ]

    for name, label, color in databases:
        dot.node(name, label, fillcolor=color, shape='cylinder')

    # 外部サービス
    dot.node('Stripe', '💳 Stripe', fillcolor=colors['external'], shape='component')
    dot.node('SendGrid', '📧 SendGrid', fillcolor=colors['external'], shape='component')
    dot.node('S3', '📦 AWS S3', fillcolor=colors['external'], shape='cylinder')

    # エッジ定義
    dot.edge('User', 'CDN', label='HTTPS')
    dot.edge('CDN', 'Web')
    dot.edge('CDN', 'Mobile')
    dot.edge('Web', 'APIGW', label='REST')
    dot.edge('Mobile', 'APIGW', label='GraphQL')

    # サービス接続
    dot.edge('APIGW', 'Auth')
    dot.edge('APIGW', 'UserSvc')
    dot.edge('APIGW', 'Product')
    dot.edge('APIGW', 'Order')
    dot.edge('APIGW', 'Payment')
    dot.edge('APIGW', 'Notification')

    # DB接続
    dot.edge('UserSvc', 'UserDB')
    dot.edge('Product', 'ProductDB')
    dot.edge('Product', 'S3', label='files')
    dot.edge('Order', 'OrderDB')
    dot.edge('Order', 'Cache')
    dot.edge('Order', 'Queue')
    dot.edge('Payment', 'Stripe', label='API')
    dot.edge('Notification', 'SendGrid', label='API')
    dot.edge('Notification', 'Queue')

    # 出力
    output_base = output_dir / "architecture_diagram"
    out = _render_or_write(dot, output_base)
    print(f"Created: {out}")
    return str(out)

def create_flowchart(output_dir: Path = Path("output/advanced")):
    """ビジネスプロセスフローチャート"""
    dot = Digraph(comment='Order Process', format='png')
    dot.attr(rankdir='LR', size='14,8', dpi='150')
    dot.attr('node', fontname='Arial', fontsize='11')
    dot.attr('edge', fontname='Arial', fontsize='9')

    # スタイル定義
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='#e3f2fd')

    # ノード
    dot.node('Start', '受注開始', shape='ellipse', fillcolor='#c8e6c9')
    dot.node('Validate', '注文検証\n・在庫確認\n・クレジットチェック')
    dot.node('Check', '在庫あり?')
    dot.node('Backorder', 'バックオーダー\n処理', fillcolor='#fff9c4')
    dot.node('Payment', '決済処理\n・Stripe API')
    dot.node('PaymentOK', '決済成功?')
    dot.node('Failed', '決済失敗\n通知', fillcolor='#ffcdd2')
    dot.node('Allocate', '在庫引当')
    dot.node('Ship', '出荷準備\n・梱包\n・配送手配')
    dot.node('Notify', '通知送信\n・メール\n・SMS')
    dot.node('End', '完了', shape='ellipse', fillcolor='#c8e6c9')

    # エッジ
    dot.edge('Start', 'Validate')
    dot.edge('Validate', 'Check')
    dot.edge('Check', 'Backorder', label='No')
    dot.edge('Check', 'Payment', label='Yes')
    dot.edge('Backorder', 'Payment')
    dot.edge('Payment', 'PaymentOK')
    dot.edge('PaymentOK', 'Failed', label='No')
    dot.edge('PaymentOK', 'Allocate', label='Yes')
    dot.edge('Failed', 'End')
    dot.edge('Allocate', 'Ship')
    dot.edge('Ship', 'Notify')
    dot.edge('Notify', 'End')

    # 出力
    output_base = output_dir / "flowchart"
    out = _render_or_write(dot, output_base)
    print(f"Created: {out}")
    return str(out)

def create_er_diagram(output_dir: Path = Path("output/advanced")):
    """ER図"""
    dot = Graph(comment='ER Diagram', format='png')
    dot.attr(rankdir='TB', size='12,10', dpi='150')
    dot.attr('node', shape='box', style='filled', fillcolor='#e8f5e9', fontname='Arial')

    # エンティティ
    entities = {
        'User': '👤 User\n-----\nPK: id\nname\nemail\npassword_hash\ncreated_at',
        'Product': '📦 Product\n-----\nPK: id\nname\ndescription\nprice\nstock',
        'Order': '📋 Order\n-----\nPK: id\nFK: user_id\ntotal_amount\nstatus\ncreated_at',
        'OrderItem': '📄 OrderItem\n-----\nPK: id\nFK: order_id\nFK: product_id\nquantity\nprice',
        'Category': '🏷 Category\n-----\nPK: id\nname\ndescription',
    }

    for name, label in entities.items():
        dot.node(name, label)

    # リレーションシップ
    dot.attr('edge', style='bold', arrowhead='none')
    dot.edge('User', 'Order', label='1:N')
    dot.edge('Order', 'OrderItem', label='1:N')
    dot.edge('Product', 'OrderItem', label='1:N')
    dot.edge('Category', 'Product', label='1:N')

    output_base = output_dir / "er_diagram"
    out = _render_or_write(dot, output_base)
    print(f"Created: {out}")
    return str(out)

def create_network_diagram(output_dir: Path = Path("output/advanced")):
    """ネットワークトポロジー図"""
    dot = Digraph(comment='Network Topology', format='png')
    dot.attr(rankdir='TB', size='12,10', dpi='150')

    # クラスタ定義
    with dot.subgraph(name='cluster_internet') as c:
        c.attr(label='Internet', style='dashed', color='gray')
        c.node('Internet', '🌐 Internet', shape='cloud')

    with dot.subgraph(name='cluster_dmz') as c:
        c.attr(label='DMZ', style='filled', color='#fff3e0', bgcolor='#fff3e0')
        c.node('Firewall1', '🛡️ Firewall', shape='box3d', fillcolor='#ffcc80')
        c.node('LB', '⚖️ Load Balancer', shape='box3d', fillcolor='#ffcc80')
        c.node('WAF', '🛡️ WAF', shape='box3d', fillcolor='#ffcc80')

    with dot.subgraph(name='cluster_app') as c:
        c.attr(label='Application Tier', style='filled', color='#e8f5e9', bgcolor='#e8f5e9')
        c.node('App1', '🖥️ App Server 1', shape='box3d', fillcolor='#a5d6a7')
        c.node('App2', '🖥️ App Server 2', shape='box3d', fillcolor='#a5d6a7')
        c.node('App3', '🖥️ App Server 3', shape='box3d', fillcolor='#a5d6a7')

    with dot.subgraph(name='cluster_db') as c:
        c.attr(label='Database Tier', style='filled', color='#fce4ec', bgcolor='#fce4ec')
        c.node('DBMaster', '🗄️ DB Master', shape='cylinder', fillcolor='#f48fb1')
        c.node('DBSlave1', '🗄️ DB Slave 1', shape='cylinder', fillcolor='#f48fb1')
        c.node('DBSlave2', '🗄️ DB Slave 2', shape='cylinder', fillcolor='#f48fb1')

    with dot.subgraph(name='cluster_cache') as c:
        c.attr(label='Cache Layer', style='filled', color='#e3f2fd', bgcolor='#e3f2fd')
        c.node('Cache1', '⚡ Redis 1', shape='cylinder', fillcolor='#90caf9')
        c.node('Cache2', '⚡ Redis 2', shape='cylinder', fillcolor='#90caf9')

    # エッジ
    dot.edge('Internet', 'Firewall1')
    dot.edge('Firewall1', 'LB')
    dot.edge('LB', 'WAF')
    dot.edge('WAF', 'App1')
    dot.edge('WAF', 'App2')
    dot.edge('WAF', 'App3')
    dot.edge('App1', 'DBMaster')
    dot.edge('App2', 'DBMaster')
    dot.edge('App3', 'DBMaster')
    dot.edge('DBMaster', 'DBSlave1', style='dashed', label='replication')
    dot.edge('DBMaster', 'DBSlave2', style='dashed', label='replication')
    dot.edge('App1', 'Cache1')
    dot.edge('App2', 'Cache1')
    dot.edge('App3', 'Cache2')

    output_base = output_dir / "network_topology"
    out = _render_or_write(dot, output_base)
    print(f"Created: {out}")
    return str(out)

def create_gantt_chart(output_dir: Path = Path("output/advanced")):
    """ガントチャート風のプロジェクトスケジュール"""
    dot = Digraph(comment='Project Schedule', format='png')
    dot.attr(rankdir='LR', size='14,8', dpi='150')
    dot.attr('node', shape='box', style='filled', fontname='Arial', fontsize='10')

    # マイルストーン
    milestones = [
        ('M1', 'M1: 要件定義\nWeek 1-2', '#c8e6c9'),
        ('M2', 'M2: 設計完了\nWeek 3-4', '#c8e6c9'),
        ('M3', 'M3: 開発完了\nWeek 5-10', '#c8e6c9'),
        ('M4', 'M4: テスト完了\nWeek 11-12', '#c8e6c9'),
        ('M5', 'M5: リリース\nWeek 13', '#ffcc80'),
    ]

    for name, label, color in milestones:
        dot.node(name, label, fillcolor=color)

    # タスク
    tasks = [
        ('T1', '環境構築\n(W1)', '#e3f2fd', 'M1'),
        ('T2', 'UI設計\n(W2)', '#e3f2fd', 'M1'),
        ('T3', 'DB設計\n(W3)', '#e3f2fd', 'M2'),
        ('T4', 'API設計\n(W4)', '#e3f2fd', 'M2'),
        ('T5', 'バックエンド\n(W5-7)', '#fff3e0', 'M3'),
        ('T6', 'フロントエンド\n(W6-8)', '#fff3e0', 'M3'),
        ('T7', '統合\n(W9-10)', '#fff3e0', 'M3'),
        ('T8', '単体テスト\n(W11)', '#fce4ec', 'M4'),
        ('T9', '結合テスト\n(W12)', '#fce4ec', 'M4'),
    ]

    for name, label, color, milestone in tasks:
        dot.node(name, label, fillcolor=color)
        dot.edge(name, milestone, style='dashed', color='gray')

    # 依存関係
    dependencies = [
        ('M1', 'M2'), ('M2', 'M3'), ('M3', 'M4'), ('M4', 'M5'),
        ('T1', 'T3'), ('T2', 'T4'), ('T3', 'T5'), ('T4', 'T5'),
        ('T5', 'T6'), ('T5', 'T7'), ('T6', 'T7'), ('T7', 'T8'),
        ('T8', 'T9'),
    ]

    for from_node, to_node in dependencies:
        dot.edge(from_node, to_node)

    output_base = output_dir / "gantt_chart"
    out = _render_or_write(dot, output_base)
    print(f"Created: {out}")
    return str(out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Graphviz diagrams (png if dot is available)")
    parser.add_argument("--output-dir", default=str(Path("output/advanced")))
    args = parser.parse_args()

    out_dir = Path(args.output_dir)

    print("Generating Graphviz diagrams...")
    if not DOT_AVAILABLE:
        print("dot executable not found. Writing DOT sources instead of rendering PNG.")

    create_system_architecture(out_dir)
    create_flowchart(out_dir)
    create_er_diagram(out_dir)
    create_network_diagram(out_dir)
    create_gantt_chart(out_dir)
    print("All diagrams generated!")
