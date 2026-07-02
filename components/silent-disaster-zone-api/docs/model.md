# 沉默風險計分與模型說明

## 目的

此元件用於排序「高風險、低觀測、低通報」而值得優先人工確認的區域。它**不**是災害預測模型，也不判定某地已發生災害。

## 正式計分：`rule_based_mvp`

正式排序由 `src/scoring/silent_risk.py` 的共享規則式函式產生，批次資料流程與即時資料流程使用相同公式，避免不同資料路徑產生不一致名次。

### 必要欄位

- `static_risk_score`
- `sensor_gap_score`
- `report_count_6h`
- `report_count_24h`

視資料可用性補入的欄位：

- `sensor_realtime_score`
- `realtime_event_score`

### 公式

```text
recent_report_score = min(report_count_6h / 3, 1)

older_report_score =
  min(max(report_count_24h - report_count_6h, 0) / 6, 1)

report_activity_score =
  0.70 × recent_report_score +
  0.30 × older_report_score

silence_factor = 1 - report_activity_score

risk_evidence_score =
  0.55 × static_risk_score +
  0.20 × sensor_realtime_score +
  0.25 × realtime_event_score

observation_gap_score = sensor_gap_score

silent_risk_score =
  risk_evidence_score ×
  (0.50 + 0.50 × observation_gap_score) ×
  silence_factor
```

### 解讀

- 靜態風險、感測異常與即時事件增加 `risk_evidence_score`。
- 感測覆蓋缺口提高資料不確定性，進而提高需要人工確認的優先度。
- 近期已驗證通報增加時，`silence_factor` 下降；這表示該區不再是「完全沉默」，而不是事件不重要。
- 已驗證通報另建立 `verified_incident_queue`，避免把「有聲但重要」的事件從決策視野中移除。

### 分級

| 等級 | 條件 |
|---|---|
| `critical` | `silent_risk_score >= 0.75` |
| `high` | `0.55 <= score < 0.75` |
| `medium` | `0.35 <= score < 0.55` |
| `low` | `score < 0.35` |

`silent_watch_queue` 的操作優先度為 P1（>=0.55）、P2（0.35–<0.55）、P3（<0.35）。

## 通報與雙隊列

### `silent_watch_queue`

來源：`silent_risk_score`。  
用途：找出低觀測與低通報下，需要主動確認的地點。

### `verified_incident_queue`

來源：人工審核為 `verified` 的通報。  
用途：顯示已有可信事件資訊、需要再研判或協調的地點。

I1 通常包含受困／需協助或嚴重程度 3；I2 為嚴重程度 2 或積淹水、土石／落石、道路中斷等；其餘為 I3。

## 神經網路實驗層

專案可保留 `silent_risk_nn_score` 與訓練腳本作為**可替換 scoring layer 的架構驗證**，但目前不應作為正式決策依據。

限制：

- 現階段使用 pseudo-label，不是真實災害 ground truth。
- 不得宣稱模型能準確預測災害或真實災情。
- 不得用 NN 分數取代 `rule_based_mvp` 正式排序。
- `model_status` 應清楚揭露模型是否被套用。

後續若有歷史災情、巡查結果、通報延遲、救災派遣紀錄與專家標註資料，可重新設計訓練、驗證、偏誤檢查與版本控管流程。

## 驗證要求

至少應檢查：

- 6 小時通報數不高於 24 小時通報數。
- 感測器缺口對排序可獨立產生影響。
- 缺少必要欄位時，流程會明確錯誤而非悄悄補成可信資料。
- live、batch、sample、unverified 各資料模式都由 metadata 明確揭露。
- 任何模型或摘要層都不可改寫正式排序或隱藏來源失敗。
