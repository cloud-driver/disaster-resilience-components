# 防災積木元件創新賽投稿說明

## 作品名稱

**沉默災區偵測 API：高風險、低觀測、低通報區域辨識元件**

## 一句話介紹

整合公開風險資料、即時事件、觀測缺口與經人工確認的通報活動，找出「最需要優先人工確認」的村里，並以標準化輸出提供儀表板、GIS、查報與派工系統使用。

## 問題描述

災情通報多的地點不一定是唯一需要關注的地點。當通訊中斷、交通受阻、感測不足、高齡人口比例較高或數位通報能力較低時，真正需要協助的地點可能反而缺少即時消息。

本元件不將「無通報」直接等同於災害，而是將它與風險證據與觀測缺口合併，建立可解釋的人工確認優先序。

## 元件類型與定位

- 類型：Service Component / API Component。
- 使用者：地方災防承辦、查報人員、GIS／儀表板開發者、巡查／志工協調者。
- 可串接：災害應變儀表板、地圖系統、LINE 回報流程、人工審核流程、巡查派工與其他防災資料平台。
- 不做：官方災害宣告、撤離命令、自動派遣或自動決定生命安全狀態。

## Input

| 資料類別 | 用途 |
|---|---|
| 村里界圖資與靜態災害風險 | 建立區域分析與基礎風險。 |
| 人口／脆弱度特徵 | 支援解釋與後續巡查任務設計。 |
| 即時雨量、警戒、道路等事件資料 | 產生當輪即時事件訊號。 |
| 感測器覆蓋與缺口 | 估計觀測不足。 |
| LINE／manual／API 通報 | 先入 `pending`，人工審核為 `verified` 後才進入正式特徵。 |

## Process

1. 抓取或讀取資料，建立單一 `run_id`。
2. 清洗、正規化並空間對應至村里。
3. 由已驗證通報建立近 6／24 小時通報特徵與已驗證事件 snapshot。
4. 使用共享的 `rule_based_mvp` 公式計算沉默風險。
5. 產生 `silent_watch_queue` 與 `verified_incident_queue`。
6. 產出 JSON、CSV、GeoJSON 與 `run_manifest.json`。
7. 若啟用 Ollama，只將既有結果整理為人可讀摘要；AI 不可改變排序或發布命令。

## Output

```text
outputs/latest/silent_risk.json
outputs/latest/silent_risk.csv
outputs/latest/silent_risk.geojson
outputs/latest/verified_incidents.json
outputs/latest/run_manifest.json
```

主要欄位：

- `village_id`、`county_name`、`town_name`、`village_name`
- `silent_risk_score`、`silent_risk_level`
- `static_risk_score`、`sensor_gap_score`、`realtime_event_score`
- `report_count_6h`、`report_count_24h`
- `scoring_mode`、`model_status`
- `meta.data_mode`、`freshness`、`run_id`、`source_status`

## API 與示範

API 路徑包含：

- `POST /auth/login`
- `GET /silent-risk`
- `GET /silent-risk/top`
- `GET /silent-risk/{village_id}`
- `GET /silent-risk.geojson`
- `GET /reports/summary`
- `GET /incidents/verified`
- `POST /line/webhook`
- `POST /pipeline/run`

完整互動文件：`/docs`。一般 API 需要短效 Bearer Token；通報審核與 pipeline 等高權限操作另需 `REPORT_ADMIN_KEY`。

## AI 使用與界線

| 可做 | 不可做 |
|---|---|
| 整理既有規則式隊列與原因 | 改變正式排序或增加／刪除村里 |
| 產生人可讀的工作摘要 | 宣稱災害已發生 |
| 進行選用實驗性架構驗證 | 發布撤離、封路、停班停課或強制派遣命令 |

神經網路實驗層目前使用 pseudo-label，只用於架構驗證；不得宣稱預測準確度，亦不得取代正式規則式排序。

## MVP 限制

- 分析範圍目前為花蓮縣村里層級。
- 外部 API、網路與資料更新會影響 live pipeline 可用性。
- LINE webhook 對外運作需要公開 HTTPS 網域與 LINE Developers 設定。
- `refresh=true` 是同步阻塞操作，正式環境應改為背景 job／排程。
- 水利署水位資料尚未完成整合。
- 路況影響仍以規則式特徵為主。
- sample 輸出只用於 demo，不能作為即時資訊。

## 延伸可能

- 將 batch／refresh 流程改為受保護的背景任務與排程。
- 以 Caddy/Nginx 與 HTTPS 部署，建立管理與稽核介面。
- 接入更多可靠的水文、交通、通訊與巡查資料。
- 使用歷史災情與現地巡查結果建立真正的標註資料與模型評估流程。
- 將結果透過母 repo 的 `IntegratedTask` contract 接入巡查或志工派工元件。
