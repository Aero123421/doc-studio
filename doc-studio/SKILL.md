---
name: doc-studio
description: PDF/PPTX/DOCX/XLSX/HTML の資料を「プロジェクト把握→ヒアリング→構成合意→案件用テンプレ作成→生成→preflight/目視チェック」まで再現可能に行うスキル。提案書/報告書/ホワイトペーパー/スライド/ダッシュボード作成に使う。
metadata:
  short-description: Generate pro docs
---

# Doc Studio

このSkillの目的は「テンプレを埋める」ことではなく、**案件・プロジェクトの中身に合わせて資料を設計し、再現可能に仕上げる**ことです。

※ コマンド例は `doc-studio/` を作業ディレクトリにして実行する前提です（リポジトリ直下から実行する場合は `doc-studio/` を前置）。

## 想定ユースケース（広め）

### 1) プロジェクト理解 → 資料化

- リポジトリを読んで、**プロジェクト概要**（目的/機能/構成/依存/運用）をまとめる
- 既存ドキュメントや設計情報を拾って、**アーキテクチャ説明資料**（PDF/PPTX）を作る
- `docs/` や `README` を元に、**社内向けオンボーディング資料**（DOCX/PDF）を作る

### 2) 依頼内容に合わせた資料作成

- 提案書/企画書（DOCX/PDF）
- 報告書/ホワイトペーパー（PDF）
- スライド（PPTX / Reveal.js HTML）
- 指標ダッシュボード（XLSX）

### 3) 既存成果物の更新

- 既存資料（DOCX/PPTX/PDF）の章立て・数値・表現を更新し、体裁を保って再生成する
- 章の差し替え/追加/削除、トーン変更、社外向け表現への変換

## 最優先ルール（テンプレ依存を断つ）

1. **生成前ゲート**: まず「プロジェクト把握」→「ヒアリング」→「構成合意」。ここを飛ばしてテンプレ選定/生成に入らない
2. **テンプレは表現・レイアウトの参考**。章立て・主張・根拠・数値・用語は案件に合わせて設計する
3. **テンプレ文言のコピペ禁止**（プレースホルダ/汎用文章を納品物に残さない）
4. 既存テンプレ（短い名前）をそのまま使うのは **ラフ用途のみ**（「ラフ」と明示し、納品前に必ず差し替える）
5. 原則として **案件用カスタムテンプレを作る**（コピーして編集する）

## Step 0: プロジェクト把握（必須）

まず「どんなプロジェクトか」「既存資産は何か」を短時間で掴む。

推奨コマンド:

```bash
python scripts/project_inspect.py --path . --depth 3
```

ここで見るもの（最低限）:

- 既存ドキュメント: `docs/`、`README*`、`*.md`、`*.docx`、`*.pptx`、`*.pdf`
- ブランド/デザイン資産: `brand/`、`design/`、`assets/`、`logo*`、色/フォント指定
- 仕様・制約: 用語集、禁止表現、コンプラ/法務注意

このStepの成果物（テキストでOK）:

- **Project Snapshot**（5〜15行）: 目的/対象ユーザー/主要機能/制約/利用技術/既存資産/トーン

## Step 1: ヒアリング（最初に聞く5問）

生成に入る前に、最低限これを確認する（ユーザーが「任せる」と言っても(1)(2)(3)は必須）。

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

## Step 2: 構成合意（生成しない）

必ず先に **構成案** を出して合意を取る。

出すもの:

- 目次（章立て）
- 各章の狙い（1行）+ 箇条書き（3〜8点）
- 「不足している情報」と「仮定一覧（明示）」  

ここで合意が取れたら、初めて生成へ進む。

## Step 3: 案件用カスタムテンプレを作る（推奨）

### 原則

- `templates/` の既存テンプレは叩き台。**そのまま使わずコピーして編集**する。
- 生成コマンドでは、短いテンプレ名よりも **テンプレファイルパス** を優先して使う。

テンプレをコピー（clone）:

```bash
python scripts/template.py clone --from whitepaper --to custom_acme_whitepaper.py
```

生成（パス指定）:

```bash
python scripts/generate.py pdf templates/custom_acme_whitepaper.py acme_whitepaper --data-file data.json
```

テンプレの必須インターフェース:

- `--output <path>` と `--data-file <path>` を受け取り、指定の出力ファイルを作成する
- 失敗時は終了コード != 0 で落ち、原因が分かるメッセージを stderr に出す

## Step 4: 生成 → preflight → 目視チェック

生成:

```bash
python scripts/generate.py <format> <template-or-path> <output> --data-file data.json
```

preflight:

```bash
python scripts/preflight.py <file>
```

目視チェックで見るもの:

- 崩れ/余白/改ページ/表の折返し
- フォント（文字化け/埋め込み/太字）
- 画像（荒れ/比率/余白）
- リンク（PDF/HTML）

## コマンド（このSkillが提供するCLI）

- プロジェクト把握: `python scripts/project_inspect.py --path .`
- テンプレ管理: `python scripts/template.py list|info|clone ...`
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
