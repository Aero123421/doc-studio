---
name: doc-studio
description: PDF/PPTX/DOCX/XLSX/HTML の資料を「要件ヒアリング→構成合意→内容に合わせたカスタム生成→preflight/目視チェック」まで再現可能に行うスキル。提案書/報告書/ホワイトペーパー/スライド/ダッシュボード作成に使う。
metadata:
  short-description: Generate pro docs
---

# Doc Studio

このSkillの目的は「テンプレを埋める」ことではなく、**案件ごとに中身を作り、再現可能な手順で資料を仕上げる**ことです。

※ コマンド例は `doc-studio/` を作業ディレクトリにして実行する前提です（リポジトリ直下から実行する場合は `doc-studio/` を前置）。

## 最優先ルール（テンプレ過依存を防ぐ）

1. **生成前に必ずヒアリングする**（最低限の質問が揃うまでテンプレ選定・生成に突入しない）
2. **テンプレは表現/レイアウトの参考**。内容（見出し・章立て・主張・根拠・数値・用語）は案件に合わせて作る
3. **テンプレ文言のコピペ禁止**（プレースホルダ/汎用文章を納品物に残さない）
4. まず **構成案（目次 + 各章の要点）** を提示し、合意を取ってから生成する
5. 情報が不足している場合は **質問するか、仮定を明示して確認**する（黙って決めない）
6. 最終成果物は **preflight + 目視チェック**（崩れ/フォント/リンク/画像/表）を通す

## ヒアリング（最初に聞く5問）

最初の返答で、まずこれだけ聞く（足りなければ次のターンで追加）。

1) **用途/読者/意思決定**
- 誰が読む？（役員/営業/技術/顧客/採用など）
- 読んだ後に何をしてほしい？（承認/購入/採用/理解/合意など）

2) **形式とボリューム**
- 形式: pdf / pptx / docx / xlsx / html
- 量: ページ数 or スライド枚数 or 文字数目安

3) **結論（先に）**
- 最も伝えたい結論は？（1行）
- サブメッセージは？（2〜5個）

4) **素材**
- 必須で入れる情報（箇条書きでOK）
- 既存資料/URL/数値/図/ロゴ/ブランドガイドの有無

5) **制約**
- トーン（硬め/カジュアル/社外向け）・NG表現・法務/コンプラ注意点
- 締切とレビュー回数

ユーザーが「任せる」と言った場合:
- 上の5問のうち **(1)(2)(3)** だけは必ず確認する
- 残りは「仮定」を明示し、後で差し替え可能にする（仮定一覧を冒頭に出す）

## 進め方（2パス推奨）

### パス1: 設計（生成しない）

1. ヒアリング回答を整理（不足があれば質問）
2. **構成案（目次 + 各章の狙い + 章ごとの箇条書き）** を提示
3. 入力データ（JSON）の案を作る（ユーザーが埋められる形にする）
4. 合意を取る（ここで初めて生成へ進む）

### パス2: 実装（生成→検査→修正）

1. テンプレは「近い表現」を参考にするだけ
2. 案件用に **カスタムテンプレを作って編集**する（推奨: `templates/custom_<案件名>.py`）
3. `scripts/generate.py` で生成
4. preflight + 目視確認
5. 指摘を反映して再生成

## テンプレの扱い方（強制的にカスタムへ寄せる）

### 原則

- `templates/` の役割は **見た目の方向性・レイアウトの参考**。
- 原則として、既存テンプレをそのまま使わず、**コピーして案件用に編集**する。

例（白紙からではなく「近い見た目」から始める）:

```bash
copy templates/pdf_whitepaper.py templates/custom_acme_whitepaper.py
python scripts/generate.py pdf templates/custom_acme_whitepaper.py acme_whitepaper --data-file data.json
```

### 例外（そのまま使って良いケース）

- ユーザーが「まずは雛形だけほしい」と明示している
- 1回目のラフとして「構成確認のため」だけに使う（納品前に必ず文章を差し替える）

## クイックスタート（確認用）

テンプレ一覧:

```bash
python scripts/template.py list
```

生成（例）:

```bash
python scripts/generate.py pdf whitepaper my_whitepaper --data-file data.json
python scripts/generate.py pptx business_modern my_slides --data-file data.json
python scripts/generate.py docx proposal my_proposal --data-file data.json
python scripts/generate.py xlsx excel_dashboard my_dashboard --data-file data.json
python scripts/generate.py html revealjs_presentation my_deck --data-file data.json
```

preflight:

```bash
python scripts/preflight.py output/pdf/my_whitepaper.pdf
```

## 生成コマンド（このSkillが提供するCLI）

- テンプレ管理: `python scripts/template.py list|info ...`
- 生成: `python scripts/generate.py <format> <template> <output> [--data|--data-file] [--engine auto|...]`
- preflight: `python scripts/preflight.py <file> [--checks ...] [--json]`
- 設定: `python scripts/config.py show|get|set|init|validate ...`

## 品質ゲート（納品前チェック）

- テンプレ由来の文章/プレースホルダが残っていない
- 結論（何を言いたいか）が冒頭1ページ/1枚で明確
- 章立てが「案件の中身」に合っている（テンプレ都合の章がない）
- 数値/固有名詞/用語が一貫している（表記揺れ無し）
- preflight を通したうえで、目視で崩れがない

## 参照

- テンプレ一覧（短い名前 → ファイル）: `references/templates.md`
- 依存関係: `references/dependencies.md`
- 設定スキーマ: `schema/config-schema.json`
