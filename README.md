<p align="right">
繁體中文 | <a href="./README.en.md">English</a>
</p>

# 讓沉默被看見：沉默災區偵測 × 志工派工元件

> 從「有人通報才處理」，轉為「主動找出高風險、低觀測、低通報的地區」，並把待確認區域轉成可供人工派工的標準任務。

本 repository 是「防災積木元件創新賽」的**整合說明與交付入口**。它不取代政府應變系統，也不是另一個完整防災平台；它整理兩個可獨立使用、可被其他系統串接的 API 元件，以及它們之間的資料契約、離線整合示範與使用限制。

## 先看這三件事

| 順序 | 元件／文件 | 用途 |
|---|---|---|
| 1 | [沉默災區偵測 API](https://github.com/cloud-driver/silent-disaster-zone-api) | 找出「值得優先人工確認」的高風險、低觀測、低通報村里；含 LINE 民眾回報、人工審核、已驗證事件隊列與資料可信度 metadata。 |
| 2 | [災害志工派工 API](https://github.com/D4rk-N355/volunteer_distributing) | 依任務急迫度、志工技能、位置與可用性，產生可人工覆核的志工候選與派工建議。 |
| 3 | [`examples/integration_demo.py`](./examples/integration_demo.py) | 使用本 repo 內建樣本資料，驗證「風險結果 → 標準任務 → 志工建議」的資料轉換流程。 |

> **事實界線：**`integration_demo.py` 是離線、樣本資料的資料層整合示範；它不會呼叫兩個子 repo 的 HTTP API，也不代表已完成正式跨服務部署。正式串接需要依本 repo 的 [資料契約](./docs/api_contract.md) 補上一層 adapter。

## 問題與解法

災害發生後，既有流程通常優先看見「已經有人回報」的地點；但斷訊、道路受阻、感測不足、高齡人口較多或數位通報門檻較高的區域，可能反而沒有能力即時發出訊息。

本作品不宣稱判定災害已發生，也不預測哪裡一定會發生災害。它做的是建立**人工確認優先序**：

```text
靜態風險＋即時事件＋觀測缺口＋近期已驗證通報活動
                         ↓
           沉默風險排序（待主動確認區域）
                         ↓
             標準化 IntegratedTask 任務
                         ↓
        志工技能／距離／可用性匹配與候選建議
                         ↓
            由具權責人員人工確認與實際派遣
```

## 元件化設計

| 元件 | Input | Process | Output | 可獨立使用？ |
|---|---|---|---|---|
| 沉默災區偵測 | 村里資料、靜態風險、感測／事件訊號、已驗證通報 | 規則式風險與沉默因子計分；區分沉默觀測隊列與已驗證事件隊列 | JSON、CSV、GeoJSON、風險 metadata、優先確認清單 | 可以 |
| 任務轉換契約 | 沉默風險結果 | 以 `IntegratedTask` 描述巡查／支援任務、位置、優先度與所需技能 | JSON Schema / OpenAPI contract | 可以 |
| 志工派工 | 任務、工作類型、志工技能／位置／可用性 | deterministic matching、距離與急迫度加權、可選 AI 異常檢查 | 派工候選、ETA、分數拆解、未指派任務與警示 | 可以 |

## 目前可驗證的成果

```bash
python3 examples/integration_demo.py
```

Windows：

```powershell
python examples\integration_demo.py
```

Demo 會讀取 `examples/sample_silent_zone_output.json` 與 `examples/sample_volunteers.json`，輸出 `examples/sample_dispatch_output.json`。它驗證：

- 將高風險、低通報區域轉成 `IntegratedTask`。
- 依所需技能、距離與可用性推薦候選志工。
- 避免同一志工在同一輪樣本任務中被重複推薦。
- 在無合適候選人或技能未完整覆蓋時，留下人工覆核警示。

## 文件導覽

| 文件 | 重點 |
|---|---|
| [快速開始](./docs/quickstart.md) | 執行本 repo 離線 demo，以及分別啟動兩個子元件。 |
| [故事與使用情境](./docs/story.md) | 角色、問題、系統不做什麼，以及從資訊缺口到人工確認的流程。 |
| [系統架構](./docs/architecture.md) | 元件邊界、資料責任與目前／目標整合狀態。 |
| [流程與圖表](./docs/diagrams.md) | Mermaid 資料流、雙隊列與部署邊界。 |
| [API 與資料契約](./docs/api_contract.md) | 真實子 API、`IntegratedTask` 與 adapter 規格。 |
| [資料來源](./docs/data_sources.md) | 靜態／即時／通報／志工資料的用途、限制與品質揭露。 |
| [AI 使用說明](./docs/ai_usage.md) | AI 實際介入的位置與不可介入的位置。 |
| [AI 治理](./docs/ai_governance.md) | 人工覆核、風險與責任界線。 |
| [限制與後續](./docs/limitations.md) | MVP 限制、資料／部署風險與下一步。 |
| [交件檢查表](./SUBMISSION_CHECKLIST.md) | 競賽交件與展示前的最後確認。 |

## 本地快照與原始碼來源

| 項目 | 本 repo 本地快照 | 上游原始 repository | 說明 |
|---|---|---|---|
| 沉默災區元件 | [`components/silent-disaster-zone-api/`](./components/silent-disaster-zone-api/) | [cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api) | 快照方便離線審閱；上游 repo 為實作真相來源。 |
| 志工派工元件 | [`components/disaster-rescuing/`](./components/disaster-rescuing/) | [D4rk-N355/volunteer_distributing](https://github.com/D4rk-N355/volunteer_distributing) | 本地資料夾保留歷史名稱 `disaster-rescuing`，但目前上游實作名稱為 `volunteer_distributing`。 |

## 非自動化決策聲明

- `silent_risk_score` 僅表示「需要優先人工確認的程度」，**不等於災害已發生**。
- `pending` 民眾回報不得直接作為正式風險排序依據；必須先完成人工審核為 `verified`。
- 志工派工結果是候選建議，不是自動派遣命令。
- AI 不得宣告災害、發布撤離／封路／停班停課命令，或取代具權責人員。
- 正式部署須額外處理授權、個資告知、資料保存、HTTPS、存取控制與稽核紀錄。

## Repository 結構

```text
.
├── README.md
├── README.en.md
├── SUBMISSION_CHECKLIST.md
├── components/
│   ├── README.md
│   ├── silent-disaster-zone-api/
│   └── disaster-rescuing/                 # 歷史資料夾名稱
├── docs/
│   ├── quickstart.md
│   ├── story.md
│   ├── architecture.md
│   ├── diagrams.md
│   ├── api_contract.md
│   ├── data_sources.md
│   ├── ai_usage.md
│   ├── ai_governance.md
│   └── limitations.md
├── examples/
│   ├── integration_demo.py
│   ├── sample_silent_zone_output.json
│   ├── sample_volunteers.json
│   └── sample_dispatch_output.json
├── schemas/
│   └── integrated_task.schema.json
└── openapi/
    └── integrated-flow-api.yaml
```

## 授權與資料

請以根目錄 `LICENSE` 為準。請勿提交 API Key、登入憑證、LINE 使用者識別碼、民眾通報原文或其他不應公開的個資。
