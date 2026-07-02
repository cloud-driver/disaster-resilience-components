# 災害志工派工 API 技術規格

> 對應上游 `D4rk-N355/volunteer_distributing` 的目前功能。實際 request／response 模型與路由請以 FastAPI 服務的 OpenAPI 為準。

## 系統概覽

服務接收災害事件、工作類型、志工與任務資料，先篩選可出勤志工，再依技能符合度、路徑距離與任務急迫度建立派工建議。結果包含指派候選、ETA、信心分數、分數拆解、未指派任務與異常警示。

## Endpoint 總覽

| Method | Endpoint | 功能 |
|---|---|---|
| `GET` | `/` | API 是否啟動。 |
| `GET` | `/health` | API 與 Ollama 狀態。 |
| `POST` | `/api/v1/dispatch` | 直接送入完整資料並立即派工。 |
| `POST` | `/api/v1/dispatch/setup` | 儲存事件與任務，不開放報名、不派工。 |
| `POST` | `/api/v1/dispatch/start` | 儲存設定、清空前輪表單、開放報名並嘗試推送群組連結。 |
| `POST` | `/api/v1/dispatch/finish` | 結束報名、合併志工資料並派工。 |
| `POST` | `/api/v1/line/register` | 登記／更新單一 LINE 志工。 |
| `POST` | `/api/v1/line/register/bulk` | 批次登記／更新 LINE 志工。 |
| `POST` | `/api/v1/line/send-group-message` | 推送測試或公告訊息到 LINE 群組。 |
| `POST` | `/webhook` | LINE Messaging API webhook。 |
| `GET` | `/volunteer/form` | 公開志工報名表。 |
| `GET` | `/volunteer/form/{line_user_id}` | 包含 LINE user ID 的個人表單。 |
| `GET` | `/webhook/volunteer/form` | 公開表單別名。 |
| `GET` | `/webhook/volunteer/form/{line_user_id}` | 個人表單別名。 |
| `POST` | `/volunteer/form/submit` | 接收 HTML 報名表。 |

## 資料模型

### `Location`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `lat` | float | 緯度。 |
| `lng` | float | 經度。 |

### `Metadata`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `incident_id` | string | 事件識別碼。 |
| `priority_weighting` | enum | `balanced`、`speed`、`expertise`。 |

### `WorkType`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `type_id` | string | 工作類型 ID，需與任務的 `type_id` 對應。 |
| `required_skills` | string[] | 執行此類工作所需技能。 |

### `Volunteer`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | string | 志工 ID。 |
| `skills` | string[] | 技能清單。 |
| `location` | `Location` | 志工位置。 |
| `availability` | boolean | 是否可出勤。 |
| `age` | int | 選填。 |
| `line_user_id` | string | 選填，用於個人通知。 |
| `special_skills` | string[] | 選填。 |

### `Task`

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | string | 任務 ID。 |
| `type_id` | string | 對應 `WorkType.type_id`。 |
| `location` | `Location` | 任務位置。 |
| `urgency` | int | 1–5，數字愈大愈急迫。 |
| `destination` | string | 選填，目的地文字。 |
| `job_description` | string | 選填，工作說明。 |

### `DispatchRequest`

```json
{
  "metadata": {
    "incident_id": "incident-2026-001",
    "priority_weighting": "balanced"
  },
  "work_types": [
    {
      "type_id": "field_check",
      "required_skills": ["field_check", "communication"]
    }
  ],
  "volunteers": [
    {
      "id": "vol_01",
      "skills": ["field_check", "communication"],
      "location": {"lat": 23.65, "lng": 121.43},
      "availability": true
    }
  ],
  "tasks": [
    {
      "id": "task_101",
      "type_id": "field_check",
      "location": {"lat": 23.66, "lng": 121.44},
      "urgency": 5,
      "job_description": "現地查核與回報"
    }
  ]
}
```

### `DispatchResponse`

| 欄位 | 說明 |
|---|---|
| `status` | 執行狀態。 |
| `dispatch_id` | 本次派工 ID。 |
| `incident_id` | 事件 ID。 |
| `mode` | `algorithm_only` 或 `algorithm_with_ai_anomaly_check`。 |
| `assignments` | 每項任務的指派結果。 |
| `unassigned_tasks` | 無法指派的任務 ID。 |
| `warnings` | 需人員注意的事項。 |

每筆 assignment 至少包含 `task_id`、`assigned_volunteers`、`eta_minutes`、`confidence`、`score_breakdown` 與 `reasoning_summary`。

## 派工規則

1. 只使用 `availability=true` 的志工。
2. 任務依 `urgency` 由高到低處理。
3. 每個任務優先取得最高分志工。
4. 剩餘志工再依最佳匹配補入。
5. 沒有可用候選人時，任務列入 `unassigned_tasks`。
6. 結果必須交由人員覆核，特別是技能未完整符合或 ETA 過長時。

### 權重

| 模式 | 技能 | 距離 | 急迫度 |
|---|---:|---:|---:|
| `balanced` | 45% | 35% | 20% |
| `speed` | 25% | 55% | 20% |
| `expertise` | 60% | 25% | 15% |

## LINE 與表單

- `/api/v1/dispatch/start` 會開放團報，並在設定完成時嘗試向 `LINE_GROUP_ID` 推送公開表單。
- `/api/v1/line/register` 在報名開放期間登記單一志工，必要時由 `GOOGLE_MAPS_API_KEY` 將地址轉座標。
- `/volunteer/form/submit` 接收表單；地址與經緯度至少需提供一種可用位置資料。
- LINE webhook 應驗證 `x-line-signature`。

## 部署提醒

此服務目前文件未定義完整對外驗證模型。正式對外時，不應裸露管理與派工 endpoint；請加上 HTTPS、反向代理、存取控制、限流、輸入驗證、日誌與稽核。
