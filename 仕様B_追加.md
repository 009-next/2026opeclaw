# 仕様B 追加要件

`仕様B_追加.txt` に記載された追加機能を、実装可能な仕様として定義します。

---

## 1. 3DビューのPPTX自動挿入

### 概要
エクスポート時、現在の3Dシーンのスクリーンショットを自動取得し、PowerPointの「現在の進捗状況（3Dビュー）」スライドに自動で挿入する。

### 現状
- `ConstructionScene.tsx` が `captureRef` 経由でスクリーンショットを取得する仕組みは実装済み
- ヘッダーの 📷 ボタンで手動キャプチャ可能
- `ExportPanel.tsx` が `screenshotDataUrl` を受け取りPPTXに挿入可能

### 追加実装内容
- `ExportPanel` のエクスポートボタン押下時、`captureRef.current?.()` を自動呼び出しし、スクリーンショットを取得してから PPTX 生成を実行する
- ユーザーが手動でキャプチャしていない場合でも、エクスポート時に自動で最新の3D画像を取得する
- WebGL の描画完了を待つため、キャプチャ後 300ms 待機してから `pptxGenerator` に渡す

### 対象ファイル
- `components/export/ExportPanel.tsx` — エクスポートボタン押下時に `captureRef.current?.()` 呼び出しを追加
- `lib/export/pptxGenerator.ts` — スライド1（現在の進捗状況）に `screenshotDataUrl` を自動挿入

---

## 2. 工程表実績の文字・図形（点と線）検知

### 概要
工程表（Excel/PDF/画像）にある赤い線・点・文字で示された「実績マーカー」を画像解析で自動検知し、タスクの実績進捗率として取り込む。

### 実装方針
- **入力**: 工程表の画像（JPEG/PNG）または PDF の各ページを画像化して Gemini マルチモーダルAPIに送信
- **処理**: Gemini に「赤い実績線・点・文字を検知し、各タスクの進捗率（0〜100）をJSON形式で返す」プロンプトを送信
- **出力**: `{ taskName: string, actualProgress: number }[]` を `ParsePreview` で確認・修正可能にする

### 新規ファイル
- `components/upload/ProgressImageUploader.tsx` — 画像ドロップ + 解析ボタン
- `app/api/detect-progress/route.ts` — Gemini マルチモーダルで実績検知
- `hooks/useProgressDetector.ts` — 画像解析状態管理

### 対象ファイル（修正）
- `app/project/[id]/page.tsx` — 「実績画像から検知」タブを左パネルに追加

---

## 3. テキスト入力欄の追加設定

### 概要
プロジェクト内の各タスクに対して、担当者・施工会社・メモなどを手入力できるテキストフィールドを追加する。また3Dシーン上でタスク名をラベル表示できるようにする。

### 追加フィールド（Task 型に追加）
```typescript
// types/project.ts への追加
interface Task {
  // ... 既存フィールド
  memo?: string;          // 自由記述メモ
  assignee?: string;      // 担当者・施工会社
  showLabel3D?: boolean;  // 3Dシーン上にラベルを表示するか
}
```

### 実装内容
- `components/dashboard/ProgressInput.tsx` に `memo` / `assignee` 入力欄を追加
- `components/scene/ConstructionScene.tsx` で `showLabel3D=true` のタスクに `<Html>` コンポーネント（Drei）でラベルをオーバーレイ表示

### 対象ファイル
- `types/project.ts` — Task 型に `memo`, `assignee`, `showLabel3D` 追加
- `components/dashboard/ProgressInput.tsx` — 入力欄追加
- `components/scene/ConstructionObject.tsx` — Drei `<Html>` ラベル追加

---

## 4. タイムラプス動画シミュレーション + PPTXへの反映

### 概要
タイムラインのシミュレーションをタイムラプス（高速スライドショー）として録画・出力し、PowerPointスライドに動画として埋め込む。

### 実装方針

#### 4-1. タイムラプス録画（クライアントサイド）
- **方式**: `canvas.captureStream()` + `MediaRecorder` API でWebM録画 または フレームキャプチャ→GIF変換
- **フロー**:
  1. 録画開始：`simulationStore.play()` を呼び出しながら `MediaRecorder.start()`
  2. 各フレームをキャプチャ（`requestAnimationFrame` 内で定期的に `gl.domElement.toDataURL()`）
  3. 録画終了：`MediaRecorder.stop()` → Blob URL を生成
- **出力形式**: WebM（Chrome/Edge）またはフレーム連結GIF（互換性優先）

#### 4-2. PPTXへの動画/GIF埋め込み
- pptxgenjs の `addImage({ data: gifDataUrl, ... })` または `addMedia({ type: "video", ... })` を使用
- GIF形式の場合は `gif.js` ライブラリでフレームを結合してデータURLに変換

### 新規ファイル
- `hooks/useTimelapsRecorder.ts` — 録画状態管理・MediaRecorder制御
- `components/scene/TimelapsControls.tsx` — 録画開始・停止ボタン

### 対象ファイル（修正）
- `lib/export/pptxGenerator.ts` — タイムラプス GIF/動画スライドを追加
- `components/export/ExportPanel.tsx` — 「タイムラプスを含める」チェックボックス追加

---

## 5. 予測画面と3Dビューアのサイズ調整

### 概要
左側パネル（入力・予測）と中央3Dビューアの幅を、ユーザーがドラッグで自由に調整できるようにする。

### 実装方針
- `react-resizable-panels` ライブラリを使用（`npm install react-resizable-panels`）
- `PanelGroup` + `Panel` + `PanelResizeHandle` で左右のレイアウトを構成

### 対象ファイル（修正）
- `app/project/[id]/page.tsx` — `<div className="flex">` を `<PanelGroup>` に置き換え

```tsx
// 実装イメージ
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";

<PanelGroup direction="horizontal">
  <Panel defaultSize={28} minSize={20} maxSize={50}>
    {/* 左パネル：入力・予測 */}
  </Panel>
  <PanelResizeHandle className="w-1 bg-slate-700 hover:bg-orange-500 cursor-col-resize transition-colors" />
  <Panel>
    {/* 中央：3Dシーン + タイムライン */}
  </Panel>
</PanelGroup>
```

---

## 優先度と依存関係

| # | 機能 | 優先度 | 依存 |
|---|---|---|---|
| 1 | 3DビューPPTX自動挿入 | 高 | 既存のcaptureRef機能 |
| 5 | パネルサイズ調整 | 高 | なし |
| 3 | テキスト入力欄追加 | 中 | Task型拡張 |
| 2 | 実績図形検知 | 中 | Geminiマルチモーダル |
| 4 | タイムラプス動画 | 低 | MediaRecorder API |

---

## 検証方法

1. **機能1**: エクスポートボタンを押す → PPTXの1枚目スライドに現在の3Dビュー画像が自動挿入されるか確認
2. **機能2**: 赤い実績線が引かれた工程表画像をアップロード → 進捗率が自動入力されるか確認
3. **機能3**: タスク一覧でメモを入力 → 3Dシーン上にラベルが表示されるか確認
4. **機能4**: 録画ボタンを押してシミュレーション再生 → GIFがダウンロードされPPTXに埋め込まれるか確認
5. **機能5**: 左右パネル境界をドラッグ → リサイズされ比率が保持されるか確認
