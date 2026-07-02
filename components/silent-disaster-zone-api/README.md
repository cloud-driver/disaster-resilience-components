# Silent Disaster Zone Detection API — 本地審閱快照

> **上游實作來源：**[cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api)  
> 本文件依目前上游實作重新整理。若本地快照程式與上游衝突，請以上游為準。

此 API 用於辨識**高風險、低觀測、低通報**的村里，協助防災人員建立「優先人工確認」清單；它同時支援 LINE 民眾災情回報、人工審核、已驗證事件快照與受限制的指揮摘要。

## 元件定位

本元件是可獨立部署的 Service Component，可接入儀表板、GIS 圖台、地方查報流程、LINE 官方帳號、巡查派工或其他防災資料平台。

它不是官方災害宣告系統、撤離命令系統或自動派遣系統。

```text
高風險 + 觀測不足 + 通報不足
              ↓
      值得優先人工確認的候選區
```

## 核心能力

- 以花蓮縣村里為目前 MVP 分析單位。
- 整合靜態災害風險、感測器覆蓋缺口、即時事件訊號與近期**已驗證**通報活動。
- 輸出 JSON、CSV、GeoJSON，並附 `data_mode`、`run_id`、`freshness`、來源狀態等 metadata。
- LINE 回報先進入 `pending`；只有人工審核為 `verified` 才會進入正式特徵與事件隊列。
- 使用 HMAC 處理 LINE user ID，避免直接保存原始識別碼。
- 正式排名使用 `rule_based_mvp`；Ollama 只可整理既有結果，不能改變排序、增刪村里、宣布災害或發布命令。
- 提供短效 Bearer Token、登入限流與高權限 `REPORT_ADMIN_KEY` 保護。

## 兩個不同的隊列

| 隊列 | 來源 | 回答的問題 | 不可混淆之處 |
|---|---|---|---|
| `silent_watch_queue` | `silent_risk_score` | 哪些地方可能因低觀測、低通報而需主動確認？ | 高分不代表災害已發生。 |
| `verified_incident_queue` | 人工審核為 `verified` 的通報 | 哪裡已有可信事件資訊，需要後續研判？ | 已有通報的地方不再是「沉默」，但仍可能急迫。 |

## 正式計分概念

```text
recent_report_score = min(report_count_6h / 3, 1)
older_report_score  = min(max(report_count_24h - report_count_6h, 0) / 6, 1)

report_activity_score = 0.70 × recent_report_score + 0.30 × older_report_score
silence_factor        = 1 - report_activity_score

risk_evidence_score =
  0.55 × static_risk_score +
  0.20 × sensor_realtime_score +
  0.25 × realtime_event_score

silent_risk_score =
  risk_evidence_score × (0.50 + 0.50 × sensor_gap_score) × silence_factor
```

分級：`critical >= 0.75`、`high >= 0.55`、`medium >= 0.35`、其餘為 `low`。此分數僅用於人員確認優先序。

## 資料可信度

主要風險 API 會回傳 `meta`：

| 欄位 | 用途 |
|---|---|
| `data_mode` | `live`、`batch`、`sample`、`unverified`。 |
| `run_id` / `generated_at` | 辨識資料處理輪次與產出時間。 |
| `freshness` | `fresh`、`stale`、`expired`、`not_realtime`、`sample_data`、`unknown`。 |
| `source_status` / `has_source_issues` | 揭露外部來源是否抓取失敗或被略過。 |
| `scoring_mode` / `model_status` | 區分正式規則排序與實驗性模型狀態。 |

不得把 `sample`、`batch` 或 `unverified` 結果說成即時災情。

## API 與啟動

建議 Python 3.12。

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

文件入口：

```text
/docs       Swagger UI
/redoc      ReDoc
/openapi.json
```

公開路由包括 `/auth/login`、`/health`、`/advisor/health`、`/line/health`、`/line/webhook` 與文件頁。其他路由需 Bearer Token；待審核通報、審核、已驗證事件、指揮建議與 pipeline 執行，另需 `X-Admin-Key`。

詳見：[API 文件](./docs/api.md)、[模型與計分](./docs/model.md)、[競賽投稿說明](./docs/submission.md)。

## 即時資料處理與輸出

```text
fetch_realtime_sources.py
  → normalize_realtime_sources.py
  → build_verified_report_features.py
  → compute_silent_risk_realtime.py
  → apply_silent_risk_nn.py
```

輸出置於：

```text
outputs/latest/silent_risk.json
outputs/latest/silent_risk.csv
outputs/latest/silent_risk.geojson
outputs/latest/verified_incidents.json
outputs/latest/run_manifest.json
```

`refresh=true` 會同步、阻塞式地跑資料流程，適合展示與內部測試；正式部署應改為受保護的排程或背景 job。

## 環境變數與安全

必要或依功能啟用的設定包含：

- `CWA_API_KEY`
- `REPORT_ADMIN_KEY`
- `REPORTER_HASH_SECRET`
- `LINE_CHANNEL_SECRET`、`LINE_CHANNEL_ACCESS_TOKEN`
- `AUTH_LOGIN_USERNAME`、`AUTH_LOGIN_PASSWORD_HASH`、`AUTH_STORAGE_SECRET`
- 可選 `OLLAMA_BASE_URL`、`OLLAMA_MODEL`

不可提交 `.env`。只有在 Uvicorn 綁定 localhost 且前方確實使用受信任的 Caddy/Nginx 時，才可考慮 `AUTH_TRUST_PROXY_HEADERS=true`。

## 與母 repo 的關係

母 repo 使用 `IntegratedTask` 來描述從沉默區風險結果生成的人工查核任務。母 repo 現有 demo 為離線樣本轉換；它不是這個 API 的即時端對端呼叫。正式整合規格見 [`../../docs/api_contract.md`](../../docs/api_contract.md)。
