# Doc Studio: 依存関係メモ

環境によって必要な依存が変わります。まずは「欲しい出力形式」と「使うテンプレ/エンジン」を決めて、必要最小限を入れるのがおすすめです。

## 前提

- Python 3
- `pip` が使えること（または同等のパッケージ管理）

## 形式別（目安）

- PPTX: `python-pptx`
- DOCX: `python-docx`（テンプレによっては `docxtpl`）
- XLSX: `XlsxWriter`
- PDF:
  - Playwright/Chromium（HTML->PDF系テンプレで使用）
  - `reportlab` / `fpdf2`（PDF直書き系テンプレで使用）
  - `weasyprint`（環境によって導入が重い。使えない場合は別エンジンに寄せる）
  - `matplotlib`（グラフ系テンプレで使用）
- preflight: `pypdf`

## Playwright（PDF生成でよく使う）

インストール:

```bash
pip install playwright
python -m playwright install chromium
```

メモ:

- 初回は Chromium のダウンロードが必要です。
- ネットワーク制限がある環境では、事前にセットアップされた環境で実行するか、別エンジンへ切り替えてください。

## Graphviz（図の生成で使用する場合）

Pythonパッケージ:

```bash
pip install graphviz
```

システムの `dot` コマンド（任意）:

- `dot` があると PNG 等へレンダリングできます。
- `dot` が無い場合でも、テンプレによっては `.dot` を書き出すフォールバックがあります。

## 依存が入れられない場合の指針

- PDFが重い: まずは Playwright(Chromium) に寄せる（導入できるなら）
- DOCX/PPTX/XLSXが必要: それぞれの最小ライブラリだけ入れる（`python-docx` / `python-pptx` / `XlsxWriter`）
- 図（Graphviz）が必要: `dot` が無理なら `.dot` 出力で納品し、相手環境でレンダリングしてもらう
