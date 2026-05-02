# Project Hooks & Scripts

Claude Codeは以下のコマンドを用いてプロジェクトのライフサイクルを管理してください。

```bash
npm run dev      # 開発サーバーの起動（Turbopack）
npm run build    # プロダクションビルドの実行
npm run lint     # コードの静的解析
```

> **注意**: `npm run mcp:start` は存在しません。MCP Blender連携は環境変数 `ENABLE_MCP_BLENDER=true` + `MCP_BLENDER_URL` を設定することで有効化されます。MCP Blenderサーバー自体はユーザーが手動で起動してください。

**Pre-computation Hook:**  
ExcelやPDFがアップロードされた際は、即座に3Dモデルを生成するのではなく、一度LLMをフックしてデータを構造化し、ユーザーに内容の確認（パース結果のプレビュー）を促すステップを挟んでください。

# カスタムフック一覧（実装済み）

| フック | ファイル | 役割 |
|---|---|---|
| `useProjectParser` | `hooks/useProjectParser.ts` | ファイル解析（Excel/PDF）→ GPT-4o → Task[] |
| `useSimulation` | `hooks/useSimulation.ts` | rAFループ・日付補間・再生制御 |
| `useTimeline` | `hooks/useTimeline.ts` | クリティカルパス・ガントレイアウト計算 |
| `use3DScene` | `hooks/use3DScene.ts` | カメラ管理・スクリーンショット取得 |
| `useDocumentGenerator` | `hooks/useDocumentGenerator.ts` | PPTX/PDF生成（3Dキャプチャ含む） |
| `useSiteConditions` | `hooks/useSiteConditions.ts` | 現地情報状態管理 + Gemini呼び出し（JPEG/PNG・5MB以内） |
| `useProgressCalculator` | `hooks/useProgressCalculator.ts` | 計画進捗率自動算出（副作用なし・純計算） |
| `useSettings` | `hooks/useSettings.ts` | APIキー・モデル名・MCP URL の読み書き（localStorage経由） |

これらのフックは再利用性・テスト容易性を重視して作成すること。

##追加項目

# 注意点
　-2026年5月2日15:30時点で作成した機能の削除は不要
　-openclawのapiで対処できない時は、"api_key.md"から各apiを自動で設定
　-自動設定したapiで予測や解析に活用

# 検証
　-ブラウザで使用する際、エラーが出ないか確認
　-エラーが出れば、解消するまで修正
　-"仕様B_追加.md"の内容を実現できているか確認
　-実現できなければ、実現できるまで修正

　
