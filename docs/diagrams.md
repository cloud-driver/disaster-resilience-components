# 系統流程圖

## 1. 完整資料流

```mermaid
flowchart TD
  A[靜態風險、村里邊界、人口特徵] --> D[資料清洗與空間標準化]
  B[即時雨量、警戒、道路／事件] --> D
  C[LINE / Manual / API 通報] --> E[pending]
  E --> F[人工審核]
  F -->|verified| G[已驗證通報特徵]
  F -->|rejected| H[保留審核紀錄，不進入正式分析]
  D --> I[風險與觀測特徵]
  G --> J[正式規則式計分]
  I --> J
  J --> K[silent_watch_queue]
  G --> L[verified_incident_queue]
  K --> M[人工確認]
  L --> M
  M --> N[IntegratedTask]
  N --> O[Adapter]
  P[志工名冊／表單／LINE 報名] --> Q[Volunteer Dispatch API]
  O --> Q
  Q --> R[候選、ETA、分數拆解、警示]
  R --> S[協調者人工決策]
```

## 2. 通報生命週期

```mermaid
stateDiagram-v2
  [*] --> pending: LINE / Manual / API report
  pending --> verified: 人工審核通過
  pending --> rejected: 人工審核拒絕
  verified --> report_features: 納入 6h / 24h 特徵
  verified --> incident_queue: 建立可信事件 snapshot
  rejected --> [*]
```

## 3. 雙隊列不可混淆

```mermaid
flowchart LR
  A[沉默風險結果] --> B[silent_watch_queue]
  C[人工 verified 通報] --> D[verified_incident_queue]
  B --> E[問題：哪裡需要主動確認？]
  D --> F[問題：哪裡已有可信事件要處理？]
  E --> G[人工建立任務]
  F --> G
```

- `silent_watch_queue`：高風險、低觀測、低通報的待確認區；不是災害宣告。
- `verified_incident_queue`：已有人為可信事件資訊；不應因為「不沉默」而被忽略。

## 4. 目前離線 demo 的實際範圍

```mermaid
flowchart LR
  A[examples/sample_silent_zone_output.json] --> B[risk_to_task]
  B --> C[IntegratedTask-like local dict]
  D[examples/sample_volunteers.json] --> E[local scoring]
  C --> E
  E --> F[examples/sample_dispatch_output.json]
```

> 這張圖描述目前 `examples/integration_demo.py` 做到的事情：它使用本機樣本 JSON 和內建 Python 邏輯，沒有呼叫子服務 HTTP endpoint。

## 5. 目標 API-to-API adapter

```mermaid
sequenceDiagram
  participant SZ as Silent Zone API
  participant AD as Integration Adapter
  participant VD as Volunteer Dispatch API
  participant CO as Human Coordinator

  CO->>SZ: 取得已驗證風險／事件結果
  SZ-->>AD: Risk result + meta + queue
  AD->>AD: 轉成 IntegratedTask，驗證 schema
  AD->>AD: priority → urgency，skills → work_types
  AD->>VD: POST /api/v1/dispatch (DispatchRequest)
  VD-->>AD: DispatchResponse
  AD-->>CO: 候選、ETA、警示與資料狀態
  CO->>CO: 人工確認是否聯繫／派遣
```

## 6. 正式部署建議

```mermaid
flowchart TB
  U[外部使用者／LINE 平台] --> RP[HTTPS Reverse Proxy]
  RP --> SZA[Silent Zone API<br/>localhost:8000]
  RP --> VDA[Volunteer API<br/>localhost:8001]
  SZA --> DB1[(通報／認證資料庫)]
  VDA --> DB2[(志工／活動／派工資料庫)]
  SZA --> JOB[受保護的背景排程]
  JOB --> EXT[外部公開資料來源]
  ADM[管理者] --> RP
```

現階段志工元件的狀態為記憶體保存；圖中的資料庫屬正式化後的目標架構。
