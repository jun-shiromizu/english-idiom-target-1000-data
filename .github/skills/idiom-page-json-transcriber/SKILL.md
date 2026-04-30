---
name: idiom-page-json-transcriber
description: 'Create target JSON files from scanned idiom-book PDFs by splitting explanation/example page pairs into one-idiom image crops and transcribing them visually instead of relying on OCR. Use when asked to build or repair target/*.json from 英熟語ターゲット1000 style scanned pages, improve low-quality OCR output, or standardize page-by-page idiom transcription workflows.'
compatibility: 'Requires Python with Pillow and rendered page images in .temp/rendered/.'
---

# Idiom Page JSON Transcriber

英熟語ターゲット1000のようなスキャン PDF から、1 熟語につき 1 つの JSON を正確に作るための Skill です。

この Skill は OCR の自動抽出を使いません。件数が多い場合でも OCR に逃げず、見開き 2 ページを 1 熟語ごとの画像に分割し、その画像を見て正確に転記する前提で使います。

OCR は下書き作成、候補抽出、穴埋め、検算のいずれの目的でも使わないでください。過去に品質の悪い JSON を量産した経緯があるため、この Skill では件数や作業量を理由に OCR を許容しません。

## When to Use This Skill

- target 配下の JSON を PDF から作成したいとき
- OCR の品質が悪く、意味・例文・注記の対応が崩れるとき
- 見開き左ページが意味、右ページが例文になっている教材を扱うとき
- 英熟語ターゲット1000のような紙面構成を 1 件ずつ確定したいとき

## Prerequisites

- 元 PDF がワークスペース内にあること
- ページ画像が .temp/rendered/page-XXX.png にあること
- Python と Pillow が使えること
- 出力仕様は .temp/prompt.md を基準に確認すること

## Workflow

1. 仕様確認

   - まず .temp/prompt.md を読む。
   - number、idioms、means、notes の構造と、読取不可時のルールを確認する。

2. ページ単位の準備

   - 見開きの説明ページと例文ページの番号を特定する。
   - 既に .temp/rendered/page-XXX.png があるならそれを使う。
   - 必要ページが未レンダリングなら、OCR ではなく PDF から追加でページ画像を用意する。

3. 1 熟語ごとの画像を作る

   - scripts/prepare_llm_crops.py を使って、見開き 2 ページを横罫線ベースで分割する。
   - 例:

   ```powershell
   python .github/skills/idiom-page-json-transcriber/scripts/prepare_llm_crops.py 16 17
   ```

   - 出力は .temp/llm-crops/pair-016-017-01.png のような形式になる。

4. 画像を見て 1 件ずつ転記する

   - 各 crop 画像は、左に見出しと意味、右に例文と日本語訳が並ぶ。
   - 画像を直接見て、推測せずに転記する。
   - synonyms は = や類義表現の欄がある場合だけ入れる。
   - notes は小さい注記、語順注記、参照注記を落とさず拾う。

5. JSON を作る

   - 1 熟語につき target/NNNN.json を 1 ファイル作る。
   - ルート要素は単一の JSON オブジェクトにする。配列で包まない。
   - 複数義があるときは means を分け、各意味に対応する例文を正しく対応付ける。

6. 検証する

   - 追加した JSON は必ず JSON として読み込めるか確認する。
   - 例:

   ```powershell
   python -c "import json, pathlib; json.load(open(pathlib.Path('target/0044.json'), encoding='utf-8')); print('ok')"
   ```

## Transcription Rules

- OCR の結果で埋めない。必ず画像を見て確定する。
- 件数が多くても OCR を使わない。作業量は OCR 使用の根拠にならない。
- 書籍の表記を優先し、勝手に言い換えない。
- 意味が 1 つでも synonyms や notes は必要なときだけ入れる。
- notes がない場合は空配列 [] を使う。
- 読めない箇所だけ [読取不可] を使い、notes に [要確認] 一部読み取り不可の箇所あり を追加する。
- 例文と和訳の対応が 1 対 1 か、複数義で対応しているかを画像で確認してから書く。

## Troubleshooting

- 画像の分割数が左右で合わない:
  説明ページと例文ページの組み合わせがずれていないか確認する。

- 横罫線の検出に失敗する:
  ページ画像が別解像度なら scripts/prepare_llm_crops.py の blue_row_score 閾値を調整する。

- OCR から直したくなる:
   この Skill の目的は OCR 補修ではなく、画像ベースでの確定入力であることを優先する。件数が多くても方針は変えない。

## Bundled Script

- [scripts/prepare_llm_crops.py](scripts/prepare_llm_crops.py)
  見開きページから 1 熟語ごとの画像を生成する。
