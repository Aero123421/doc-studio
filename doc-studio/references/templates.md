# Doc Studio: テンプレ一覧

まずは一覧を表示:

```bash
python scripts/template.py list
```

このファイルは「どのテンプレ名がどのファイルに対応しているか」を手早く確認するためのメモです。

## `generate` コマンドで使えるテンプレ（短い名前）

`python scripts/generate.py <format> <template> <output> ...` の `<template>` に指定できます。

### PDF

- `whitepaper` -> `templates/pdf_whitepaper.py`
- `catalog` -> `templates/pdf_catalog.py`
- `portfolio` -> `templates/pdf_portfolio.py`
- `infographic` -> `templates/pdf_infographic.py`
- `flyer` -> `templates/pdf_flyer.py`
- `reportlab_advanced` -> `templates/advanced_reportlab.py`
- `weasyprint_premium` -> `templates/advanced_weasyprint.py`
- `matplotlib_datareport` -> `templates/advanced_matplotlib.py`
- `fpdf2_modern` -> `templates/advanced_fpdf2.py`
- `proposal_template` -> `templates/advanced_docxtpl.py`

### PPTX

- `business_modern` -> `templates/pptx_business_modern.py`
- `creative_gradient` -> `templates/pptx_creative_gradient.py`
- `technical_dark` -> `templates/pptx_technical_dark.py`
- `minimalist` -> `templates/pptx_minimalist.py`
- `corporate_formal` -> `templates/pptx_corporate_formal.py`
- `advanced_business` -> `templates/pptx_advanced_business.py`

### DOCX

- `proposal` -> `templates/docx_proposal.py`
- `manual` -> `templates/docx_manual.py`
- `resume` -> `templates/docx_resume.py`

### XLSX

- `excel_dashboard` -> `templates/advanced_xlsxwriter.py`

### HTML

- `revealjs_presentation` -> `templates/html_revealjs_presentation.py`

## テンプレ指定のコツ

`<template>` には以下も指定できます（要件に応じて自由に）:

- テンプレファイル名: `pdf_whitepaper.py`
- `templates/` からの相対パス: `templates/pdf_whitepaper.py`
- 絶対パス: `C:\path\to\my_template.py`

## 単体実行のサンプル（`generate` とは別）

以下は `scripts/generate.py` のインターフェース（`--output`/`--data-file`）とは別の、単体スクリプトです。

- Graphviz図の生成: `templates/advanced_graphviz.py`

例:

```bash
python templates/advanced_graphviz.py --output-dir output/advanced
```
