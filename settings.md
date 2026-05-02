# Project Settings & Configuration

このファイルは、ウェブブラウザアプリの動作環境、API連携、およびアプリケーション固有のパラメータを定義します。

---

## 1. LLM Service Configuration

仕様B.txtに基づき、以下の3つのモデルを役割に応じて使い分けます。

| Provider | 使用モデル | Primary Role |
| :--- | :--- | :--- |
| **Anthropic** | `claude-sonnet-4-6` | 進捗予測・遅延分析・複雑な推論 |
| **OpenAI** | `gpt-4o` | 工程表テキストの構造化JSONパース |
| **Google** | `gemini-2.0-flash` | 現地情報のマルチモーダル解析（テキスト+画像） |

> モデル名はUIの設定パネルまたは環境変数で変更可能。

---

## 2. UI からの設定（SettingsPanel）

APIキーとモデル名はブラウザUIの設定パネルからも入力・保存できます。

- **アクセス方法**: アプリヘッダーの ⚙ アイコンをクリック
- **保存先**: `localStorage`（`sitesim3d:settings` キー）
- **実装**: `lib/storage/settingsStorage.ts` + `hooks/useSettings.ts` + `components/settings/SettingsPanel.tsx`

設定可能な項目：

| 項目 | デフォルト値 |
| :--- | :--- |
| Anthropic API Key | （空） |
| OpenAI API Key | （空） |
| Google API Key | （空） |
| Anthropic Model | `claude-sonnet-4-6` |
| OpenAI Model | `gpt-4o` |
| Gemini Model | `gemini-2.0-flash` |
| MCP Blender URL | `http://localhost:8000` |

UIで設定したAPIキーは `useSettings().apiHeaders()` でリクエストヘッダに付与され、API Routeが `req.headers.get("x-anthropic-key")` 等で読み取って使用します。`.env.local` のキーはフォールバックとして機能します。

---

## 3. Environment Variables (.env.local)

```env
# LLM API Keys（UIから設定した場合はそちらが優先）
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key

# LLM モデル名（UIから変更した場合はそちらが優先）
ANTHROPIC_MODEL=claude-sonnet-4-6
OPENAI_MODEL=gpt-4o
GEMINI_MODEL=gemini-2.0-flash

# MCP Blender（オプション・ローカル利用のみ）
MCP_BLENDER_URL=http://localhost:8000
ENABLE_MCP_BLENDER=false

# Opus モードの有効化（高精度・低速）
ENABLE_OPUS=false
```

> **セキュリティ注意**: `NEXT_PUBLIC_` プレフィックスは付けないこと。全LLMキーはサーバーサイド（API Route）でのみ使用する。

---

## 4. 対応ファイル形式

```
SUPPORTED_FILE_TYPES: [".pdf", ".xlsx", ".xls"]
EXPORT_FORMATS: ["pptx", "pdf"]
DEFAULT_LANGUAGE: "japanese"
```

---

## 5. アプリ情報

- **名称**: SiteSim3D（工事進捗3Dシミュレーター）
- **バージョン**: 0.1.0
- **言語**: TypeScript / Japanese UI
- **ターゲット**: PCブラウザ（Chrome推奨）+ PWA（デスクトップインストール可能）

---

## 6. 開発モード設定

- Strict Mode: `true`
- Tailwind CSS: `true`
- ESLint: 厳格設定
- 3Dデバッグ: `AxesHelper`, `Stats` 表示（開発時のみ）
- PWA: `disable: process.env.NODE_ENV === "development"`（開発時は無効）

---

## 7. 将来拡張

- ユーザーアカウント / 複数プロジェクト管理
- AIによる工程最適化提案（Gemini/Claude連携）
- 実際のBIMモデル（IFC）対応
- VRモード
