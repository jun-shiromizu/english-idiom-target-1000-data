
---
name: idiom-image-add
description: 'Add idiom-related image links to supplement/NNNN-add.md by matching the target idiom, its main verb, and its preposition against bundled reference files. Use when asked to attach images to supplement markdown, enrich idiom explanations with image links, or process one or more target numbers using .github/skills/idiom-image-add/references/idioms.md, verb.json, and prep.json.'
compatibility: 'Requires target/NNNN.json, supplement/NNNN-add.md, and image reference files under .github/skills/idiom-image-add/references/.'
---

# Idiom Image Add

target 配下の各 JSON に対応する supplement の Markdown に、熟語画像へのリンクを追記する Skill です。

この Skill は、対象熟語そのものに対応する画像に加えて、熟語を構成する動詞と前置詞に対応する画像も探し、supplement/NNNN-add.md に ### 画像 セクションとして追加します。

## When to Use This Skill

- supplement/NNNN-add.md に画像リンクを追加したいとき
- 特定の熟語番号に対して、対応する視覚イメージを補足資料に埋め込みたいとき
- .github/skills/idiom-image-add/references/idioms.md と verb.json と prep.json を使って画像候補を引きたいとき
- 既存の supplement Markdown を保ちつつ、画像セクションだけ追加・更新したいとき

## Inputs

- ユーザーから熟語番号を受け取る。番号は 1 から 1000 を想定する。
- 対象熟語は target/NNNN.json から特定する。
- 出力先は supplement/NNNN-add.md とする。

## References

- 熟語画像の対応表: .github/skills/idiom-image-add/references/idioms.md
- 動詞画像の対応表: .github/skills/idiom-image-add/references/verb.json
- 前置詞画像の対応表: .github/skills/idiom-image-add/references/prep.json

## Workflow

1. 対象熟語を特定する

   - ユーザーが指定した番号に対応する target/NNNN.json を開く。
   - JSON から対象の熟語を取得する。

2. 熟語に対応する画像を探す

   - .github/skills/idiom-image-add/references/idioms.md を見て、熟語に対応する画像名を探す。
   - 例えば add-up.png は add up に対応する。
   - 1 つの熟語に複数画像がある場合がある。例えば break into に break-into.png と break-into-2.png がある。
   - 1 つの画像が複数熟語に対応する場合もある。例えば drop-fall-away.png は drop away と fall away に対応する。

3. 熟語画像がない場合の扱いを決める

   - 熟語そのものに対応する画像が存在しない場合は、その熟語については処理を終了する。
   - 動詞画像と前置詞画像の探索、および Markdown 追記は行わない。
   - 複数番号を処理している場合は、次の熟語へ進む。

4. 動詞に対応する画像を探す

   - 熟語の主要な動詞を取り出す。例えば come about の動詞は come である。
   - .github/skills/idiom-image-add/references/verb.json から、その動詞に対応する画像を探す。

5. 前置詞に対応する画像を探す

   - 熟語の主要な前置詞を取り出す。例えば come about の前置詞は about である。
   - .github/skills/idiom-image-add/references/prep.json から、その前置詞に対応する画像を探す。

6. supplement Markdown に画像を追記する

   - 対象ファイルは supplement/NNNN-add.md とする。
   - 既存の説明は保持し、その末尾または適切な位置に ### 画像 セクションを追加する。
   - 画像の並び順は、熟語、動詞、前置詞の順にする。

## Output Format

supplement/NNNN-add.md には、少なくとも次のようなセクションがある想定です。

```markdown
### 連想

a piece of は、piece「切り取られた一部分」 + of「〜の」＝ 大きなもの・数えにくいものから切り出した1つ ⇒ 1つの〜、というイメージ。

paper や advice のように、そのままでは数えにくい名詞でも、a piece of を前に置くと「1枚」「1つ」のように数えられる形にできる。

### 類義語
- a piece of
  - 不可算名詞を「1つ分」に区切って数えるときの基本表現
  - a piece of paper のように、形のあるものにも抽象的なものにも使える
- one
  - すでに数えられる名詞に対して「1つ」を表す
  - one paper だと「新聞・論文1部」のように、paper を可算名詞として扱う意味になりやすい
- an item of
  - information や news などを「1項目」として数えるときに使う
  - a piece of より少し整理された情報・項目という感じが強い
```

画像セクションは次の形式で追加する。

```markdown
### 画像
<!-- 熟語に対応する画像 -->
![](../img/drop-off.png)
![](../img/drop-off2.png)

<!-- 動詞に対応する画像 -->
![](../img/drop-fall.png)
![](../img/drop-fall2.png)

<!-- 前置詞に対応する画像 -->
![](../img/off.png)
![](../img/off2.png)
```

## Rules

- 画像を貼る順番は、熟語、動詞、前置詞の順に固定する。
- 画像パスは supplement からの相対パスとして ../img/<filename> を使う。
- 該当画像がない区分は空のままにせず、その区分の画像行自体を出さない。
- 既に ### 画像 セクションがある場合は、重複追記ではなく内容を確認して整理する。
- 対象熟語そのものの画像がない場合は、動詞・前置詞画像だけで補完しない。

## Validation

- target/NNNN.json から取得した熟語と、追加した画像が対応していることを確認する。
- supplement/NNNN-add.md に ### 画像 が追加されていることを確認する。
- 画像リンクの順序が、熟語、動詞、前置詞になっていることを確認する。
- 画像ファイル名が references の対応表と一致していることを確認する。
