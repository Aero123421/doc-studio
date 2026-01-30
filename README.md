# Doc Studio Skill

このリポジトリは「doc-studio」Skill（PDF/PPTX/DOCX/XLSX/HTML などの資料生成 + preflight）を提供します。

Skill本体は `doc-studio/` フォルダです（Skillフォルダ内に README を置かない方針のため、README はリポジトリ直下に置いています）。

## Quick start

```bash
cd doc-studio
python scripts/template.py list
python scripts/generate.py pdf whitepaper my_whitepaper --data-file data.json
python scripts/preflight.py output/pdf/my_whitepaper.pdf
```

## Install（各CLIへコピー）

例（Codex CLI）:

```bash
python doc-studio/install.py install --cli codex
```

他:

```bash
python doc-studio/install.py install --cli claude-code
python doc-studio/install.py install --cli gemini
python doc-studio/install.py install --cli opencode
```
