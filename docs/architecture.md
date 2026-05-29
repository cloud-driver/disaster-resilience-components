<p align="right">
繁體中文 | [English](architecture.en.md)
</p>

# 系統架構

## 1. 架構定位

本專案採用「主整合 repo + 兩個獨立 API 元件」的設計。

```text
主整合 repo
負責說明故事、架構、API 契約、AI 使用方式與限制
        │
        ├── Component A: Silent Disaster Zone Detection API
        │       負責偵測高風險但低通報的沉默災區
        │
        └── Component B: Disaster Volunteer Dispatcher API
                負責根據任務與志工資料產生派遣建議
```

這樣做的原因是：兩個元件功能邊界清楚，不應硬塞成單一後端。保留獨立元件可以讓其他災防系統只採用其中一個，也可以完整串接兩個元件形成救災決策鏈。

## 2. 高層資料流

```text
[公開資料 / 即時資料 / 通報資料]
        ↓
[沉默災區偵測 API]
        ↓
[高風險低通報區域清單 + GeoJSON]
        ↓
[任務產生器：巡查、確認、救援、物資]
        ↓
[救災志工智慧分配 API]
        ↓
[派遣建議：任務 ID、志工 ID、ETA、原因]
        ↓
[人類指揮者確認]
        ↓
[現地回報 / 任務結果]
        ↓
[回流成通報資料與模型改善資料]
```

## 3. Component A：沉默災區偵測 API

### 3.1 功能

此元件用來產生村里層級的沉默風險分數。它將「災害風險」與「通報落差」結合，找出那些看起來應該被確認、但目前缺乏通報或觀測資料的區域。

### 3.2 輸入資料

| 類型 | 格式 | 用途 |
|---|---|---|
| 村里界 | GeoJSON / Shapefile | 建立空間分析單位 |
| 人口與年齡結構 | CSV | 評估脆弱度，例如高齡人口比例 |
| 淹水潛勢 | GeoJSON / Shapefile | 建立靜態災害風險 |
| 土石流資料 | GeoJSON / Shapefile / API snapshot | 建立山區風險訊號 |
| 即時雨量 | JSON API snapshot | 建立即時事件訊號 |
| 即時路況 | JSON API snapshot | 判斷交通中斷可能性 |
| 災情通報 | JSON | 計算近期通報量與通報落差 |

### 3.3 處理邏輯

```text
Static risk features
    = village boundary + population + flood potential + debris flow data

Realtime event features
    = rainfall + landslide alert + road events

Report features
    = report count in recent time windows

Silent risk score
    = high risk signal × low report activity / observation gap
```

### 3.4 輸出

| 輸出 | 格式 | 說明 |
|---|---|---|
| `silent_risk.json` | JSON | API 查詢用資料 |
| `silent_risk.csv` | CSV | 人工檢查與表格分析 |
| `silent_risk.geojson` | GeoJSON | 地圖系統圖層 |

## 4. Component B：救災志工智慧分配 API

### 4.1 功能

此元件接收任務與志工資料，產生派遣建議。它的核心任務不是取代指揮官，而是降低人工同時計算技能、距離、可用性與緊急度的負擔。

### 4.2 輸入資料

| 類型 | 欄位 | 用途 |
|---|---|---|
| metadata | incident_id, priority_weighting | 設定事件與調度模式 |
| work_types | type_id, required_skills | 定義任務類型與所需技能 |
| volunteers | id, skills, location, availability | 描述可用志工 |
| tasks | id, type_id, location, urgency | 描述待處理任務 |

### 4.3 處理邏輯

```text
接收任務與志工資料
        ↓
過濾可用志工
        ↓
依任務緊急度排序
        ↓
計算志工與任務距離
        ↓
使用 Ollama 派發模型產生建議
        ↓
如 AI 回應無效，使用偵錯模型或本地演算法
        ↓
輸出派遣清單
```

### 4.4 降級設計

如果 Ollama 無法連線、模型不存在、推理逾時或回應格式不可用，系統會改用本地演算法：

```text
可用志工 → 技能 / 距離優先 → 最近或最合適志工 → ETA → 派遣結果
```

這是重要設計，因為災害場景不能假設 AI 永遠可用。

## 5. 兩元件整合方式

### 5.1 概念整合

沉默災區偵測 API 的輸出可以被轉成 Dispatcher API 的任務輸入。

例如：

```json
{
  "village_id": "10015020001",
  "county_name": "花蓮縣",
  "town_name": "鳳林鎮",
  "village_name": "鳳仁里",
  "silent_risk_score": 0.392821,
  "silent_risk_level": "medium",
  "silent_reason": "靜態災害風險偏高；感測器覆蓋缺口偏高；近6小時無通報"
}
```

可以轉成：

```json
{
  "id": "task_check_10015020001",
  "type_id": "FieldCheck",
  "location": {
    "lat": 23.75,
    "lng": 121.45
  },
  "urgency": 4
}
```

### 5.2 實作建議

MVP 階段可先用一個簡單轉換器：

```text
silent_risk_level = high   → urgency = 5
silent_risk_level = medium → urgency = 4
silent_risk_level = low    → urgency = 2
```

正式版可加入更多規則，例如：

- 高齡人口比例高 → 優先派有急救或照護經驗者
- 道路事件明顯 → 任務類型改為 RoadCheck
- 土石流訊號強 → 任務類型改為 HazardVerification
- 通訊中斷可能性高 → 優先聯絡村里長、消防分隊或鄰近志工

## 6. 部署架構建議

### 6.1 MVP 部署

```text
Local Machine
├── FastAPI: Silent Disaster Zone Detection API
├── FastAPI: Disaster Volunteer Dispatcher API
└── Ollama: Local LLM runtime
```

### 6.2 Demo 部署

```text
Browser / Swagger UI
        ↓
FastAPI services
        ↓
Sample outputs / mock data
        ↓
Optional local Ollama
```

### 6.3 未來部署

```text
Dashboard / LINE Bot / Google Chat
        ↓
API Gateway
        ↓
Silent Disaster Zone Detection API
        ↓
Task Generator
        ↓
Volunteer Dispatcher API
        ↓
Incident Management System
```

## 7. 架構原則

1. **元件邊界清楚**：偵測與派遣分開。
2. **資料格式標準化**：使用 JSON、CSV、GeoJSON。
3. **可獨立運作**：每個 API 都能單獨被其他系統呼叫。
4. **可人工審核**：AI 不直接做最終災害決策。
5. **可降級運作**：AI 不可用時仍能有基本功能。
