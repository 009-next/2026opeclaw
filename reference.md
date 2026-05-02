# Application Reference & Workflows

## Data Flow

1. **Input Phase:**
   - ユーザー：作業/工事名を入力。
   - ユーザー：工程表（Excel/PDF）をアップロード。
   - ユーザー：現在の日時、および現在の「実績（進捗度合い）」を入力。
   - ユーザー：現地の土地情報（テキストまたは画像）を入力。

2. **Processing Phase:**
   - **GPT-4o**（`/api/parse-schedule`）：工程表テキストを解析し、タスクの階層構造とスケジュールをJSON化。
   - **Gemini**（`/api/site-analysis`）：土地情報を解析し、注意点や提案テキストをマルチモーダルで生成。
   - **Three.js（Tier 1・全ユーザー）**：タスクの進捗率に応じた工種別プロシージャルモデルをクライアント側でリアルタイム生成。
   - **MCP Blender（Tier 2・オプション）**：`ENABLE_MCP_BLENDER=true` 時のみ、`/api/generate-3d` 経由で Blender MCPサーバーに3Dモデル生成をプロキシ。

3. **Output Phase:**
   - Frontend：Three.js / React Three Fiber で3Dモデルをブラウザにレンダリング。
   - **Claude**（`/api/predict`）：現在の3Dモデルと工程表から、今後の展開を予測するシミュレーションを実行。
   - Export：3DビューのキャプチャURL、予測テキスト、土地の注意点をまとめ、PowerPointまたはPDF資料を生成。

## API キーの流れ

```
ユーザー → SettingsPanel（UIで入力）
        → localStorage に保存（settingsStorage）
        → useSettings().apiHeaders() でリクエストヘッダに付与
        → Next.js API Route（サーバーサイド）
        → req.headers.get("x-anthropic-key") 等で読み取り
        → LLMクライアント（Anthropic / OpenAI / Google）に渡す
        → .env.local のキーが設定されている場合はフォールバックとして使用
```

# リファレンス・参考実装

## 3D関連

- React Three Fiber 公式ドキュメント
- Three.js Journey（進捗可視化向けアニメーション）
- 工事現場3D表現例（重機、足場、建物段階的構築）

## 工程表処理

- SheetJS + ZodによるExcelバリデーション
- 工程表 → タスクツリー変換ロジック

## 資料生成

- pptxgenjs 使用例
- jsPDF ドキュメント

## UI/UX参考

- 建設業向けダッシュボード（進捗3D + タイムライン）
- Blender風3Dビューコントロール（OrbitControls + TransformControls）
