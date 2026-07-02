# Silent Disaster Zone Detection API 文件

> 本文件對應目前上游實作。完整欄位、必填性與範例以服務啟動後的 `/docs` 為準。

## Base URL 與文件

本機開發預設：

```text
http://127.0.0.1:8000
```

```text
/docs          Swagger UI
/redoc         ReDoc
/openapi.json  OpenAPI JSON
```

## 驗證模型

### 公開路由

| Method | Path | 用途 |
|---|---|---|
| `POST` | `/auth/login` | 登入並取得短效 Token。 |
| `GET` | `/health` | API、資料集與模型狀態。 |
| `GET` | `/advisor/health` | 選用 Ollama advisor 狀態。 |
| `GET` | `/line/health` | LINE 設定狀態。 |
| `POST` | `/line/webhook` | LINE webhook；以 `X-Line-Signature` 驗證。 |
| `GET` | `/docs`、`/redoc`、`/openapi.json` | 文件入口。 |

### Bearer Token

除上述路由外，所有 API 都需要：

```http
Authorization: Bearer <access_token>
```

Token 成功登入後有效 15 分鐘，登出後失效；同一 IP 對 `/auth/login` 在 60 秒內最多 5 次。

### 高權限操作

以下路由除 Bearer Token 外，還需要：

```http
X-Admin-Key: <REPORT_ADMIN_KEY>
```

- `GET /reports/pending`
- `POST /reports/{report_id}/review`
- `GET /incidents/verified`
- `GET /advisor/command`
- `POST /pipeline/run`

## Endpoint 總覽

| 編號 | Method | Path | 用途 |
|---|---|---|---|
| 00-1 | `GET` | `/` | API 入口資訊。 |
| 00-2 | `GET` | `/health` | API、資料輸出與選用模型狀態。 |
| 00-3 | `GET` | `/model/info` | 實驗模型 metadata。 |
| 01-1 | `POST` | `/auth/login` | 取得 15 分鐘 Token。 |
| 01-2 | `GET` | `/auth/session` | 查詢目前登入狀態。 |
| 01-3 | `POST` | `/auth/logout` | 撤銷目前 Token。 |
| 10-1 | `GET` | `/silent-risk` | 沉默風險清單與篩選。 |
| 10-2 | `GET` | `/silent-risk/top` | 最高風險候選區域。 |
| 10-3 | `GET` | `/silent-risk/{village_id}` | 單一村里結果。 |
| 10-4 | `GET` | `/silent-risk.geojson` | 地圖 GeoJSON。 |
| 20-1 | `GET` | `/advisor/health` | advisor 健康檢查。 |
| 20-2 | `GET` | `/advisor/command` | 雙隊列的指揮輔助資料。 |
| 30-1 | `GET` | `/reports/summary` | 民眾回報統計。 |
| 30-2 | `GET` | `/reports/pending` | 待人工審核通報。 |
| 30-3 | `POST` | `/reports/{report_id}/review` | 審核 `verified`／`rejected`。 |
| 40-1 | `GET` | `/incidents/verified` | 已驗證事件 snapshot。 |
| 50-1 | `GET` | `/line/health` | LINE 健康檢查。 |
| 50-2 | `POST` | `/line/webhook` | LINE webhook。 |
| 90-1 | `POST` | `/pipeline/run` | 受保護的完整 batch pipeline。 |

## 常用範例

登入：

```bash
TOKEN=$(
  curl -s -X POST http://127.0.0.1:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"api-admin","password":"your-password"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])'
)
```

查詢前 5 名待確認區域：

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  "http://127.0.0.1:8000/silent-risk/top?limit=5"
```

取得地圖資料：

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  "http://127.0.0.1:8000/silent-risk.geojson"
```

查看待審核通報：

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Admin-Key: $REPORT_ADMIN_KEY" \
  "http://127.0.0.1:8000/reports/pending?limit=20"
```

## `refresh=true` 的限制

`/silent-risk`、`/silent-risk/top` 與 `/advisor/command` 可使用 `refresh=true` 觸發同步資料流程。此操作：

- 會阻塞請求。
- 依賴外部資料、網路與本機環境。
- 適合展示或內部測試，不適合讓未受信任使用者重複呼叫。
- 正式環境應改由排程／背景 job 產生 `outputs/latest/`，查詢 API 僅讀取已驗證產出。

## 回應 metadata

任何風險輸出都必須先讀取 `meta.data_mode`、`freshness`、`run_id` 與 `source_status`。`sample`、`batch` 或 `unverified` 不能被宣稱為即時資料。

## 回應碼

| Code | 意義 |
|---:|---|
| 200 | 成功。 |
| 401 | Bearer Token 缺失、無效、過期或已撤銷。 |
| 403 | `REPORT_ADMIN_KEY` 缺失或無效。 |
| 404 | 資源、輸出檔或 snapshot 不存在。 |
| 409 | 狀態衝突，例如重複審核已非 `pending` 的回報。 |
| 422 | 欄位或參數格式錯誤。 |
| 429 | 登入請求超過限流。 |
| 500 | pipeline 或伺服器處理失敗。 |
| 503 | 必要環境設定未完成。 |

## 重要安全邊界

- `silent_risk_score` 是確認優先序，不是災害宣告。
- `pending` 回報不可直接進入正式排序。
- `verified` 表示完成人工查證，但仍不等於官方宣告。
- API 或 AI 輸出不得直接用於撤離、封路、停班停課、強制資源調度等命令。
