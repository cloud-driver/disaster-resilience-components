<p align="right">
繁體中文 | <a href="./api_contract.en.md">English</a>
</p>

# API 契約

本文定義兩個元件在整合時應遵守的輸入、輸出與資料交換格式。實際欄位可依各 component repository 的 OpenAPI / Swagger 文件為準；此文件主要用於主提案 repo 說明兩元件如何拼接。

## 1. Component A：Silent Disaster Zone Detection API

### 1.1 目的

輸出村里層級的沉默風險資料，供地圖、儀表板、任務產生器或派遣系統讀取。

### 1.2 主要 endpoints

| Method | Endpoint | 說明 |
|---|---|---|
| GET | `/health` | 檢查 API 與輸出資料可用狀態 |
| GET | `/model/info` | 回傳神經網路 scoring layer 的模型 metadata |
| GET | `/silent-risk/top?limit=5` | 回傳沉默風險最高的前 N 個村里 |
| GET | `/silent-risk/top?limit=5&refresh=true` | 重新抓取即時資料並計算風險，適合開發或 demo |
| GET | `/silent-risk/{village_id}` | 查詢單一村里的沉默風險資料 |
| GET | `/silent-risk.geojson` | 回傳可供地圖顯示的 GeoJSON 圖層 |

### 1.3 `GET /silent-risk/top` 範例回應

```json
{
  "status": "success",
  "data": [
    {
      "village_id": "10015020001",
      "county_name": "花蓮縣",
      "town_name": "鳳林鎮",
      "village_name": "鳳仁里",
      "silent_risk_score": 0.392821,
      "silent_risk_level": "medium",
      "silent_reason": "靜態災害風險偏高；感測器覆蓋缺口偏高；近6小時無通報；近24小時無通報",
      "silent_risk_rule_score": 0.41,
      "silent_risk_nn_score": 0.39,
      "static_risk_score": 0.61,
      "sensor_gap_score": 0.61,
      "realtime_event_score": 0.0,
      "report_count_6h": 0,
      "report_count_24h": 0
    }
  ]
}
```

### 1.4 欄位說明

| 欄位 | 型別 | 說明 |
|---|---|---|
| `village_id` | string | 村里識別碼 |
| `county_name` | string | 縣市名稱 |
| `town_name` | string | 鄉鎮市區名稱 |
| `village_name` | string | 村里名稱 |
| `silent_risk_score` | number | 最終沉默風險分數 |
| `silent_risk_level` | string | 風險等級，例如 `low`、`medium`、`high` |
| `silent_reason` | string | 可讀的原因摘要 |
| `silent_risk_rule_score` | number | 規則式基準分數 |
| `silent_risk_nn_score` | number | 神經網路 scoring layer 分數 |
| `static_risk_score` | number | 靜態風險分數 |
| `sensor_gap_score` | number | 感測器或觀測覆蓋缺口分數 |
| `realtime_event_score` | number | 即時事件訊號分數 |
| `report_count_6h` | integer | 近 6 小時通報數 |
| `report_count_24h` | integer | 近 24 小時通報數 |

## 2. Component B：Disaster Volunteer Dispatcher API

### 2.1 目的

接收任務與志工資料，輸出建議派遣結果。

### 2.2 主要 endpoints

| Method | Endpoint | 說明 |
|---|---|---|
| GET | `/` | API 基本狀態訊息 |
| GET | `/health` | 檢查 API 與 Ollama 服務狀態 |
| POST | `/api/v1/dispatch/v1` | 建立派遣計畫 |

### 2.3 `POST /api/v1/dispatch/v1` 請求格式

```json
{
  "metadata": {
    "incident_id": "mataian-2025-001",
    "priority_weighting": "balanced"
  },
  "work_types": [
    {
      "type_id": "FieldCheck",
      "required_skills": ["FirstAid", "LocalGuide"]
    },
    {
      "type_id": "Logistics",
      "required_skills": ["HeavyLifting"]
    }
  ],
  "volunteers": [
    {
      "id": "vol_01",
      "skills": ["FirstAid", "LocalGuide"],
      "location": {
        "lat": 23.654,
        "lng": 121.432
      },
      "availability": true
    },
    {
      "id": "vol_02",
      "skills": ["HeavyLifting"],
      "location": {
        "lat": 23.660,
        "lng": 121.440
      },
      "availability": true
    }
  ],
  "tasks": [
    {
      "id": "task_check_10015020001",
      "type_id": "FieldCheck",
      "location": {
        "lat": 23.656,
        "lng": 121.435
      },
      "urgency": 4
    }
  ]
}
```

### 2.4 請求欄位說明

| 欄位 | 型別 | 說明 |
|---|---|---|
| `metadata.incident_id` | string | 災害事件或調度批次識別碼 |
| `metadata.priority_weighting` | string | 調度權重模式：`balanced`、`speed`、`expertise` |
| `work_types[].type_id` | string | 任務類型識別碼 |
| `work_types[].required_skills` | string[] | 該任務類型需要的技能標籤 |
| `volunteers[].id` | string | 去識別化志工 ID |
| `volunteers[].skills` | string[] | 志工技能標籤 |
| `volunteers[].location.lat` | number | 緯度 |
| `volunteers[].location.lng` | number | 經度 |
| `volunteers[].availability` | boolean | 是否可出勤 |
| `tasks[].id` | string | 任務 ID |
| `tasks[].type_id` | string | 任務類型 |
| `tasks[].location.lat` | number | 任務地點緯度 |
| `tasks[].location.lng` | number | 任務地點經度 |
| `tasks[].urgency` | integer | 緊急程度，1 到 5 |

### 2.5 回應格式

```json
{
  "status": "success",
  "dispatch_id": "uuid-xxx",
  "assignments": [
    {
      "task_id": "task_check_10015020001",
      "assigned_volunteers": ["vol_01"],
      "eta_minutes": 15,
      "reasoning_summary": "[Ollama-派發] 指派 vol_01，原因是具備 FirstAid 與 LocalGuide，且距離任務地點較近。"
    }
  ]
}
```

### 2.6 回應欄位說明

| 欄位 | 型別 | 說明 |
|---|---|---|
| `status` | string | 執行狀態 |
| `dispatch_id` | string | 派遣批次 ID |
| `assignments[].task_id` | string | 任務 ID |
| `assignments[].assigned_volunteers` | string[] | 被指派的志工 ID |
| `assignments[].eta_minutes` | integer | 預估抵達時間，單位分鐘 |
| `assignments[].reasoning_summary` | string | AI 或本地演算法的摘要說明 |

## 3. 兩元件之間的轉換契約

沉默災區偵測 API 的輸出不應直接等於派遣命令。中間需要一層「任務產生」轉換邏輯。

### 3.1 轉換規則 MVP

| Silent risk output | Task input |
|---|---|
| `village_id` | `task.id = task_check_{village_id}` |
| `silent_risk_level = high` | `urgency = 5` |
| `silent_risk_level = medium` | `urgency = 4` |
| `silent_risk_level = low` | `urgency = 2` |
| `silent_reason` 包含道路、通訊、弱勢等關鍵字 | 可影響 `type_id` |
| GeoJSON centroid 或村里中心點 | `task.location` |

### 3.2 任務類型建議

| type_id | 說明 | 所需技能建議 |
|---|---|---|
| `FieldCheck` | 現地狀況確認 | LocalGuide, FirstAid |
| `RoadCheck` | 道路可通行確認 | LocalGuide, Driving |
| `MedicalCheck` | 弱勢或傷病確認 | FirstAid, EMT |
| `Logistics` | 物資搬運 | HeavyLifting, Logistics |
| `CommunicationCheck` | 通訊與聯絡確認 | Radio, LocalGuide |

## 4. 錯誤處理建議

| 狀況 | 建議行為 |
|---|---|
| 沉默災區 API 無輸出 | 使用 sample output 或提示資料尚未準備 |
| 即時資料來源失敗 | 保留上次成功 snapshot，並標記資料時間 |
| Dispatcher API 沒有可用志工 | 回傳空 assigned_volunteers，並要求人工補派 |
| Ollama 無法連線 | 使用本地演算法 fallback |
| AI 回應無法解析 | 使用偵錯模型或本地演算法 fallback |
| 任務地點缺少經緯度 | 不進行自動派遣，要求人工補齊座標 |
