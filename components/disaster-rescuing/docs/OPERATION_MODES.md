# 操作模式與限制

## 共通前提

兩條路徑最後都把志工資料整理為 `Volunteer`，搭配同一份事件與任務設定執行派工。所有派工結果都應由協調者人工確認。

> **目前限制：**待派工設定、報名開關與表單投稿保存在記憶體。服務重啟後資料會遺失；正式環境必須改為持久化資料庫並保留稽核紀錄。

## 模式一：整合表單團報

### 適用情境

主辦端已建立某事件的任務清單，想在 LINE 群組、社群或其他管道發送同一份公開表單，快速收集多人報名。

### 流程

1. 管理者準備 `DispatchSetupRequest`，包含 `metadata`、`work_types`、`tasks`。
2. 呼叫：

   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/dispatch/start \
     -H "Content-Type: application/json" \
     -d @event_declaration_example.json
   ```

3. 系統清空前一輪投稿、儲存事件與任務、開放報名，並嘗試推送：

   ```text
   {APP_BASE_URL}/volunteer/form
   ```

4. 志工填寫姓名、技能、位置與是否可出勤。位置可填地址，或直接填經緯度。
5. 管理者確認收件結束，呼叫：

   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/dispatch/finish
   ```

6. 系統關閉報名、合併公開表單與已登記 LINE 志工、執行派工並嘗試推送摘要。

### 特性

- 適合大型、臨時與來源分散的志工動員。
- 不要求每個人都有 LINE user ID。
- 沒有 `line_user_id` 時，後續只能依填寫名稱識別，無法可靠地個別通知。
- 使用地址轉座標必須設定 `GOOGLE_MAPS_API_KEY`。

## 模式二：志工個人報名

### 適用情境

已有 LINE Bot 好友、固定志工隊或外部名冊，希望保留個別 LINE user ID 以便後續通知與更新資料。

### 路徑 A：API 登記

1. 先以 `/api/v1/dispatch/start` 開放報名，或以 `/api/v1/dispatch/setup` 建立事件後再由其他流程開放。
2. 登記單一志工：

   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/line/register \
     -H "Content-Type: application/json" \
     -d '{
       "line_user_id": "U1234567890abcdef",
       "display_name": "王小明",
       "skills": ["field_check", "logistics"],
       "location": {"lat": 25.033964, "lng": 121.564468},
       "availability": true
     }'
   ```

3. 需要匯入名冊時，使用 `/api/v1/line/register/bulk`。
4. 收件結束後呼叫 `/api/v1/dispatch/finish`。

### 路徑 B：個人表單

1. 系統或 LINE Bot 提供：

   ```text
   {APP_BASE_URL}/volunteer/form/{line_user_id}
   ```

2. 志工補齊名稱、技能與位置。
3. 表單送至 `/volunteer/form/submit`。
4. 管理者呼叫 `/api/v1/dispatch/finish`。

### 特性

- 可維持個人 LINE 對應，較適合後續通知與資料更新。
- 目前登記操作需在報名開放期間。
- 同一 `line_user_id` 重複登記時，會更新既有資料。

## 兩種模式比較

| 項目 | 團報 | 個人報名 |
|---|---|---|
| 主要入口 | `/api/v1/dispatch/start` + `/volunteer/form` | `/api/v1/line/register` 或 `/volunteer/form/{line_user_id}` |
| 是否需要 LINE user ID | 不一定 | 建議需要 |
| 適合規模 | 多人、臨時 | 單人、既有名冊 |
| 身分辨識 | 顯示名稱或 LINE ID | LINE ID 為主 |
| 個人通知 | 較弱 | 較完整 |
| 收斂點 | `/api/v1/dispatch/finish` | `/api/v1/dispatch/finish` |

## 操作風險與防呆

- 報名未開放時，表單送出應被拒絕。
- 地址轉座標失敗時，應改要求完整經緯度，而不是建立未知位置的志工。
- 指派結果中的 `warnings`、`unassigned_tasks`、技能缺口與 ETA 必須讓人工協調者看到。
- LINE／地圖／Ollama 設定失敗不能讓核心 deterministic dispatch 靜默失敗；應回傳可追蹤警示。
- 正式部署時，活動設定、志工資料與派工歷程應持久化並加入權限、審計與資料保存期限。
