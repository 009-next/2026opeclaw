# Required Skills & Tech Stack

## Frontend

- **Framework:** Next.js 16 (App Router + Turbopack) / TypeScript
- **UI Component:** Tailwind CSS / shadcn/ui（現場担当者が直感的に操作できるシンプルなUI）
- **3D Rendering:** Three.js / React Three Fiber / Drei（工種別プロシージャルモデル + OrbitControls）
- **File Parsing:** SheetJS (`xlsx`) — Excel解析、`pdfjs-dist` — PDFテキスト抽出

## Backend & Integration

- **API Routes:** Next.js App Router の `route.ts` でLLM呼び出しをサーバーサイドにカプセル化
- **3D Modeling（Tier 2・オプション）:** `ENABLE_MCP_BLENDER=true` 時のみ `/api/generate-3d` 経由で MCP Blender にプロキシ
- **LLM APIs:**
  - Anthropic API（`claude-sonnet-4-6`）— 進捗予測・遅延分析
  - OpenAI API（`gpt-4o`）— 工程表の構造化JSON解析
  - Google Gemini API（`gemini-2.0-flash`）— 現地情報マルチモーダル解析
- **Document Generation:** `pptxgenjs`（PPTXエクスポート）、`jsPDF`（PDFエクスポート）
- **Storage:** IndexedDB (`idb`) — プロジェクトデータ永続化、localStorage — アプリ設定（APIキー・モデル名）

## System Architecture

```
Browser (Next.js App Router)
│
├── Client-side のみ
│   ├── SheetJS → Excel解析
│   ├── pdfjs-dist → PDFテキスト抽出
│   ├── Three.js / R3F → WebGL 3Dシーン
│   ├── pptxgenjs / jsPDF → 資料生成
│   ├── Zustand → 全状態管理
│   ├── IndexedDB → プロジェクト永続化
│   └── localStorage → 設定（APIキー・モデル名・MCP URL）
│
└── Next.js API Routes（サーバーサイド・APIキー保護）
    ├── POST /api/parse-schedule  → GPT-4o（工程表 → Task[]）
    ├── POST /api/predict         → claude-sonnet-4-6（進捗予測）
    ├── POST /api/site-analysis   → gemini-2.0-flash（現地解析）
    └── POST /api/generate-3d    → MCP Blenderプロキシ（ENABLE_MCP_BLENDER=true 時のみ）
```

# カスタムフック一覧（実装済み）

| フック | ファイル | 役割 |
|---|---|---|
| `useProjectParser` | `hooks/useProjectParser.ts` | ファイル解析 → LLM → Task[] |
| `useSimulation` | `hooks/useSimulation.ts` | rAFループ・日付補間・再生制御 |
| `useTimeline` | `hooks/useTimeline.ts` | クリティカルパス・ガントレイアウト |
| `use3DScene` | `hooks/use3DScene.ts` | カメラ管理・スクリーンショット取得 |
| `useDocumentGenerator` | `hooks/useDocumentGenerator.ts` | PPTX/PDF生成（3Dキャプチャ含む） |
| `useSiteConditions` | `hooks/useSiteConditions.ts` | 現地情報状態 + Gemini呼び出し |
| `useProgressCalculator` | `hooks/useProgressCalculator.ts` | 計画進捗率自動算出（純計算） |
| `useSettings` | `hooks/useSettings.ts` | APIキー・モデル名・MCP URL の読み書き |

# Claudeが活用すべきスキルセット

## 必須スキル

- Next.js 16 + React Server Components の最新ベストプラクティス
- Three.js / @react-three/fiber での複雑な3Dシーン構築
- 工程表の自動解析・Gantt Chart + 3D連動
- タイムラインと3Dモデルの同期アニメーション
- ファイルアップロード（Excel, PDF, 画像）
- 動的PPTX/PDF生成
- PWA設定（manifest, service worker）

## 開発ルール

- 常にTypeScript厳格モード
- コンポーネントはshadcn/uiをベースに拡張
- 3Dシーンはパフォーマンス最適化必須（LOD, Instancing検討）
- タブレット・PC対応（レスポンシブ）
- ダークモード標準対応
- アクセシビリティ配慮
