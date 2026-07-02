# 災害志工派工 API — 本地審閱快照

> **上游實作來源：**[D4rk-N355/volunteer_distributing](https://github.com/D4rk-N355/volunteer_distributing)  
> 本地資料夾維持歷史名稱 `disaster-rescuing`，但目前上游 repository 名稱為 `volunteer_distributing`。若快照與上游衝突，請以上游為準。

這是一個以 FastAPI 建置的災害志工派工服務。它接收事件、工作類型、任務與志工資料，依**技能、距離、急迫度與可用性**產生 deterministic dispatch 建議；可選擇使用 LINE 公告、公開報名表、個人報名連結與 Ollama 異常檢查。

## 元件定位

此服務回答的是：

> 在已有人員確認任務需求後，哪些可出勤志工是較合理的候選人？

它是人員協調與決策支援元件，**不是**自動救援派遣、官方指揮系統或生命安全判定系統。最終是否派遣、如何派遣、是否需要專業救援單位，仍由具權責人員決定。

## 主要能力

- 只納入 `availability=true` 的志工。
- 任務依 `urgency`（1–5）由高至低處理。
- 依技能、距離、急迫度產生指派分數與理由。
- 支援三種加權：`balanced`、`speed`、`expertise`。
- 輸出 ETA、信心分數、分數拆解、未指派任務與警示。
- 選用 Ollama 進行異常檢查；Ollama 不可用時，服務維持 `algorithm_only`。
- 支援兩種招募流程：公開表單團報、LINE／API 個人報名。
- LINE 群組可接收公開報名連結與派工摘要。
- 地址轉座標需要 `GOOGLE_MAPS_API_KEY`；沒有 key 時可直接填經緯度。

## 兩條操作路徑

| 路徑 | 適合情境 | 核心流程 |
|---|---|---|
| 整合表單團報 | 臨時、大量、來源分散的志工 | `/api/v1/dispatch/start` → `/volunteer/form` → `/api/v1/dispatch/finish` |
| 志工個人報名 | 已有 LINE Bot 好友或既有志工名冊 | `/api/v1/line/register`／個人表單 → `/api/v1/dispatch/finish` |

## 快速啟動

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

健康檢查：

```bash
curl http://127.0.0.1:8000/health
```

直接派工：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/dispatch \
  -H "Content-Type: application/json" \
  -d @sample_payloads.json
```

## 基本資料模型

```text
DispatchRequest
├── metadata: incident_id, priority_weighting
├── work_types: type_id, required_skills
├── volunteers: id, skills, location, availability, ...
└── tasks: id, type_id, location, urgency, ...
```

輸出 `DispatchResponse` 會包含：

- `assignments`
- `unassigned_tasks`
- `warnings`
- 每一任務的 `eta_minutes`、`confidence`、`score_breakdown` 與 `reasoning_summary`

完整欄位請看 [技術規格](./docs/SPECIFICATION.md)。

## 加權模式

| 模式 | 技能 | 距離 | 急迫度 | 適用說明 |
|---|---:|---:|---:|---|
| `balanced` | 45% | 35% | 20% | 一般情境的折衷。 |
| `speed` | 25% | 55% | 20% | 優先縮短到場距離。 |
| `expertise` | 60% | 25% | 15% | 優先專業技能匹配。 |

## 重要限制與安全

- 服務目前以**記憶體**保存待派工設定與報名資料，重啟後會遺失。
- 公開報名表在報名未開放時應拒絕送出。
- 未設定 LINE 相關環境變數時，派工核心仍可運作，但不會完成 LINE 推播。
- 本服務的公開 API 文件尚未定義完整對外身份驗證／授權機制。正式公開部署前，應在反向代理層加上 HTTPS、存取控制、限流、稽核與管理介面保護。
- Ollama 僅做可選的異常檢查，不參與核心派工決策。
- 建議保留人工覆核，特別是高急迫度、技能不完整、ETA 過長或無候選人的任務。

## 與母 repo 的關係

母 repo 定義 `IntegratedTask` 作為從沉默風險結果轉換出的標準任務格式。它與此服務的 `DispatchRequest` 不完全相同，正式整合需要 adapter 來：

1. 將 `IntegratedTask.task.priority` 轉成 `Task.urgency`（1–5）。
2. 將 `required_skills` 建成對應的 `WorkType.required_skills`。
3. 將 `task.task_type` 對應為 Dispatcher 的 `Task.type_id`。
4. 提供實際志工資料與 `Metadata`。

詳見 [`../../docs/api_contract.md`](../../docs/api_contract.md)。
