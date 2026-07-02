# 快速開始

## 0. 先理解你要驗證什麼

本母 repo 目前可直接驗證的是**離線資料流**：

```text
sample_silent_zone_output.json
  → IntegratedTask
  → sample_volunteers.json
  → sample_dispatch_output.json
```

它不需要 API Key，也不啟動兩個子服務；因此不能被當作 API-to-API 部署證明。

## 1. 執行母 repo 的離線整合 demo

需求：Python 3.10+（demo 僅使用標準函式庫）。

macOS / Linux：

```bash
python3 examples/integration_demo.py
```

Windows：

```powershell
python examples\integration_demo.py
```

預期輸出：

```text
examples/sample_dispatch_output.json
```

檢查重點：

- 有產生任務與候選志工。
- 同一志工沒有在同一輪 demo 中被重複推薦。
- 無合適候選人或技能覆蓋不足時有 `warning`。
- 輸出內容僅是 sample 資料推導，不代表現況災情。

## 2. 啟動沉默災區偵測元件

上游 repo：

```bash
git clone https://github.com/cloud-driver/silent-disaster-zone-api.git
cd silent-disaster-zone-api

python3 -m venv .venv
source .venv/bin/activate        # Windows 改用 .\.venv\Scripts\Activate.ps1
python3 -m pip install -r requirements.txt
cp .env.example .env             # Windows 改用 Copy-Item .env.example .env
```

至少設定登入與管理所需的環境變數。即時資料與 LINE 功能另需相關 API／secret。

啟動：

```bash
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

查看：

```text
http://127.0.0.1:8000/docs
```

先用 `/health` 確認資料模式。只有 `meta.data_mode=live` 且來源狀態正常時，才能把結果當成當輪即時人工確認參考。

## 3. 啟動志工派工元件

上游 repo：

```bash
git clone https://github.com/D4rk-N355/volunteer_distributing.git
cd volunteer_distributing

python -m pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8001
```

> 使用 `8001` 是為了避免和沉默元件的 `8000` 衝突。

健康檢查：

```bash
curl http://127.0.0.1:8001/health
```

直接派工：

```bash
curl -X POST http://127.0.0.1:8001/api/v1/dispatch \
  -H "Content-Type: application/json" \
  -d @sample_payloads.json
```

## 4. 正式串接前的最低要求

母 repo 目前沒有可直接執行的 HTTP adapter。要做端對端串接，至少需：

1. 從沉默元件取得已驗證的風險結果與 metadata。
2. 選擇 `silent_watch_queue` 或 `verified_incident_queue`，不可混為同一種風險。
3. 將結果轉為 `IntegratedTask`。
4. 將 `IntegratedTask` 轉為志工元件的 `DispatchRequest`：
   - `priority` → `urgency`（1–5）。
   - `task_type` → `type_id`。
   - `required_skills` → `work_types[].required_skills`。
   - 加入實際可用的志工名冊。
5. 把候選結果交由人工協調者覆核後，再進行實際聯繫或派遣。

詳見：[API 與資料契約](./api_contract.md)。

## 5. 正式部署前不要跳過的項目

- 以 Caddy／Nginx 反向代理提供 HTTPS。
- 不直接公開管理 endpoint 或 `.env`。
- 啟用存取控制、限流、日誌與稽核。
- 將志工元件的記憶體狀態改為持久化資料庫。
- 將沉默元件 `refresh=true` 的同步流程改為受保護的背景 job／排程。
- 建立個資告知、保存期間與刪除機制。
