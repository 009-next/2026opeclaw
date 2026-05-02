# Git Worktree Strategy — SiteSim3D

このプロジェクトでは、複数の主要機能が相互に影響し合うため、`git worktree` を使用して環境を分離し、並行して開発・検証を行います。

---

## 0. 前提：Git リポジトリの初期化

`sitesim3d/` はまだ git リポジトリではないため、開発開始前に以下を実行します。

```bash
cd sitesim3d/

git init
git add .
git commit -m "feat: initial SiteSim3D implementation"
```

`.gitignore` に以下が含まれていることを確認してください。

```
.env.local
node_modules/
.next/
```

---

## 1. Directory Structure

ワークツリーは `sitesim3d/` と同階層の `worktrees/` ディレクトリ内に作成します。

```
202605/
├── sitesim3d/          ← main ブランチ（本体リポジトリ）
├── planB/              ← 仕様ドキュメント
└── worktrees/          ← worktree 作業ディレクトリ
    ├── feat-3d-sim/        3Dシーン改善・新工種追加
    ├── feat-llm/           LLM 3種の精度向上・プロンプト調整
    ├── feat-doc-gen/       PPTX/PDF エクスポート強化
    └── feat-land-analysis/ 現地情報解析（Gemini マルチモーダル）
```

---

## 2. Worktree Commands

### ワークツリーの作成

```bash
# 3Dシミュレーション機能の改善
git -C sitesim3d worktree add ../worktrees/feat-3d-sim -b feature/3d-simulation

# LLM 統合（Claude / GPT-4o / Gemini）改善
git -C sitesim3d worktree add ../worktrees/feat-llm -b feature/llm-integration

# PPTX / PDF 資料生成強化
git -C sitesim3d worktree add ../worktrees/feat-doc-gen -b feature/doc-generation

# 土地情報・現地条件解析強化
git -C sitesim3d worktree add ../worktrees/feat-land-analysis -b feature/land-analysis
```

### ワークツリーの確認

```bash
git -C sitesim3d worktree list
```

### ワークツリーの削除（作業完了後）

```bash
# ワークツリーディレクトリを削除してから参照を解除
rm -rf worktrees/feat-3d-sim
git -C sitesim3d worktree prune
```

---

## 3. Branch Strategy

| ブランチ名 | 用途 |
|---|---|
| `main` | 本番・安定版。動作確認済みのコードのみ |
| `feature/3d-simulation` | Three.js シーン改善、新工種（トンネル等）の3D表現 |
| `feature/llm-integration` | プロンプト最適化、モデル切り替え、レスポンスキャッシュ |
| `feature/doc-generation` | PPTX スライドデザイン改善、PDF レイアウト強化 |
| `feature/land-analysis` | Gemini マルチモーダル解析、画像からの地形推定 |

### マージフロー

```
feature/* → main
```

各 feature ブランチは `npm run build` が通ることを確認してから main にマージします。

---

## 4. 各ワークツリーの担当ファイル

### `feat-3d-sim/`（3D シーン）

```
components/scene/
  ConstructionScene.tsx    ← カメラ・照明・影の改善
  ConstructionObject.tsx   ← マテリアル・アニメーション追加
  ProceduralBuilding.tsx   ← 工種ごとの詳細ジオメトリ
  ProceduralRoad.tsx
  ProceduralBridge.tsx
  ProceduralEarthwork.tsx
lib/3d/
  constructionTypes.ts     ← 工種別ジオメトリ戦略の追加
  proceduralModels.ts      ← パラメータ計算ロジック改善
```

### `feat-llm/`（LLM 統合）

```
lib/llm/
  claude.ts      ← extended thinking の有効化、プロンプト改善
  openai.ts      ← structured output スキーマの精緻化
  gemini.ts      ← マルチモーダル入力の強化
app/api/
  parse-schedule/route.ts
  predict/route.ts
  site-analysis/route.ts
```

### `feat-doc-gen/`（資料生成）

```
lib/export/
  pptxGenerator.ts   ← スライドデザイン・グラフ追加
  pdfGenerator.ts    ← レイアウト・フォント改善
components/export/
  ExportPanel.tsx    ← オプション（スライド枚数等）追加
```

### `feat-land-analysis/`（現地解析）

```
lib/llm/gemini.ts            ← 画像解析プロンプト強化
hooks/useSiteConditions.ts   ← 複数画像対応
components/dashboard/
  SiteConditions.tsx         ← 画像プレビュー・複数枚対応
```

---

## 5. 作業フロー（Claude Code 向け）

```
1. 担当機能のワークツリーに移動
   cd worktrees/feat-3d-sim/

2. 最新の main を取り込む
   git merge main

3. 実装・テスト
   npm run dev  →  動作確認
   npm run build  →  ビルド確認
   npx tsc --noEmit  →  型チェック

4. コミット
   git add <変更ファイル>
   git commit -m "feat(3d): add tunnel geometry stages"

5. main にマージ
   cd ../../sitesim3d/
   git merge feature/3d-simulation

6. ワークツリーを削除（任意）
   rm -rf ../worktrees/feat-3d-sim
   git worktree prune
```

---

## 6. 注意事項

- **同一ブランチを複数 worktree で同時チェックアウトしない**（git の制約）
- **node_modules は各 worktree に独立して存在**するため、worktree 作成後に `npm install` が必要
- **`.env.local` は各 worktree にコピー**する（gitignore されているため自動コピーされない）
- **`public/pdf.worker.min.mjs`** も worktree にコピーが必要（`node_modules` 外のファイルのため）

```bash
# worktree 初期セットアップ（新しいワークツリー作成直後に実行）
cd worktrees/feat-3d-sim/
npm install
cp ../../sitesim3d/.env.local .env.local
cp ../../sitesim3d/public/pdf.worker.min.mjs public/pdf.worker.min.mjs
```

---

## 7. 推奨ディレクトリ構成（実運用）

```
202605/
├── sitesim3d/              ← main ブランチ本体
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── store/
│   ├── types/
│   ├── public/
│   ├── .env.local          ← gitignore（各自管理）
│   └── package.json
│
├── worktrees/              ← git worktree 作業ディレクトリ
│   ├── feat-3d-sim/
│   ├── feat-llm/
│   ├── feat-doc-gen/
│   └── feat-land-analysis/
│
└── planB/                  ← 仕様ドキュメント（非コード）
    ├── claude.md
    ├── skill.md
    ├── reference.md
    ├── rules.md
    ├── settings.md
    ├── hooks.md
    ├── git-worktree.md     ← このファイル
    └── 仕様B.txt
```
