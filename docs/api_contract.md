# API 與資料交換契約

## 核心結論

母 repo 定義的 `IntegratedTask` 是**正規化中間格式**，用來把沉默風險結果描述成可交給下游系統處理的任務。它不是目前志工派工 API 可直接接收的 request body。

目前可驗證的服務：

| 元件 | 主要 API | 驗證／安全現況 |
|---|---|---|
| 沉默災區偵測 | `/silent-risk`、`/reports/*`、`/incidents/verified`、`/advisor/command` | 大多數 API 需短效 Bearer；管理操作另需 `REPORT_ADMIN_KEY`。 |
| 志工派工 | `/api/v1/dispatch`、`/api/v1/dispatch/start`、`/api/v1/dispatch/finish`、表單與 LINE webhook | 核心派工功能存在；公開部署前需補足外部授權、持久化與反向代理保護。 |
| 母 repo | `schemas/integrated_task.schema.json`、`openapi/integrated-flow-api.yaml` | Schema 和 OpenAPI 是整合規格；`/integrated-flow/dispatch-recommendations` 尚未部署。 |

## `IntegratedTask`

Schema 檔案：[`../schemas/integrated_task.schema.json`](../schemas/integrated_task.schema.json)。

最小概念：

```json
{
  "task_id": "TASK-HL-V001",
  "source_component": "silent-disaster-zone-api",
  "area": {
    "county": "花蓮縣",
    "town": "光復鄉",
    "village": "大安村"
  },
  "risk": {
    "silent_risk_score": 0.91,
    "risk_level": "critical",
    "reasons": ["高淹水風險", "通報數偏低"]
  },
  "task": {
    "task_type": "field_check",
    "priority": "urgent",
    "description": "請前往花蓮縣光復鄉大安村確認是否有未通報災情。"
  },
  "location": {
    "lat": 23.6651,
    "lng": 121.4213
  },
  "required_skills": ["field_check", "communication"]
}
```

## Adapter 轉換規格

### Step 1：選擇來源 queue

| 來源 | 可建立的任務類型 | 需要保留的說明 |
|---|---|---|
| `silent_watch_queue` | `field_check`、`road_status_check`、視情況 `medical_support` | 是「主動確認」，不能描述成已確認災情。 |
| `verified_incident_queue` | 視事件類型建立 `medical_support`、`supply_delivery`、`road_status_check` 等 | 是已人工審核事件，但仍不是官方災害宣告。 |

### Step 2：`IntegratedTask` → Dispatcher `DispatchRequest`

| `IntegratedTask` | DispatchRequest | 轉換規則 |
|---|---|---|
| `task_id` | `tasks[].id` | 直接映射。 |
| `task.task_type` | `tasks[].type_id` | 使用明確工作類型表。 |
| `location` | `tasks[].location` | 直接映射。 |
| `task.priority` | `tasks[].urgency` | `low=2`、`medium=3`、`high=4`、`urgent=5`；值可配置但必須記錄。 |
| `required_skills` | `work_types[].required_skills` | 依 `type_id` 建立或合併。 |
| `task.description` | `tasks[].job_description` | 直接映射，附上資料模式與確認需求。 |
| `risk`／`area` | job description、任務 audit metadata | 目前 Dispatcher 模型沒有對應必填欄位，不可丟失。 |
| 志工名冊 | `volunteers[]` | 由已授權且最新的志工資料提供。 |
| event context | `metadata.incident_id`、`priority_weighting` | 由協調者／事件管理程序建立。 |

### 轉換後的 request 範例

```json
{
  "metadata": {
    "incident_id": "hualien-demo-001",
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
      "id": "vol-01",
      "skills": ["field_check", "communication"],
      "location": {"lat": 23.67, "lng": 121.43},
      "availability": true
    }
  ],
  "tasks": [
    {
      "id": "TASK-HL-V001",
      "type_id": "field_check",
      "location": {"lat": 23.6651, "lng": 121.4213},
      "urgency": 5,
      "job_description": "主動查核候選區；需人工確認，不代表已發生災害。"
    }
  ]
}
```

## Response 契約與人工覆核

志工服務回應應至少保留：

- `assignments`
- `eta_minutes`
- `confidence`
- `score_breakdown`
- `reasoning_summary`
- `unassigned_tasks`
- `warnings`

adapter 或 UI 不可只顯示「推薦志工」而隱藏 `warnings`、資料模式、距離與技能缺口。

## OpenAPI 文件的地位

[`../openapi/integrated-flow-api.yaml`](../openapi/integrated-flow-api.yaml) 描述目標 endpoint：

```text
POST /integrated-flow/dispatch-recommendations
```

這份檔案是為未來整合 façade 準備的合約。**本 repo 目前沒有實作或部署此 endpoint。**此外，其示例 Volunteer schema 與上游志工服務的 `Volunteer` 模型不同；實作時必須先統一或明確轉換。

## 最低驗證流程

1. 從沉默元件讀取資料及 `meta`。
2. 拒絕／標示 `sample`、`unverified`、過期或來源失敗的資料。
3. 對每個轉換後任務使用 JSON Schema 驗證。
4. 建構 `DispatchRequest` 並呼叫志工元件。
5. 保存 request、response、時間、資料 `run_id`、操作人與警示。
6. 由人工協調者確認後，才進入對外通知或實際派遣。
