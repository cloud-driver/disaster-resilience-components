<p align="right">
繁體中文 | <a href="./README.en.md">English</a>
</p>

# 雙元件防災決策鏈

> **沉默災區偵測 API × 救災志工智慧分配 API**  
> 找出可能被忽略的高風險區域，並把確認、巡查或救援任務派給最適合的志工。

本專案是為「防災積木元件創新賽：公民科技拼出韌性臺灣」整理的**主提案 / 整合展示 repository**。它不是一個封閉的大型平台，而是一組可獨立部署、可重複使用、可與其他防災系統拼接的 API 元件組合。

## 1. 為什麼要做這兩個功能？

災害發生後，指揮中心最容易看到的是「有通報的地方」：哪裡淹水、哪裡道路中斷、哪裡缺物資。

但真正危險的區域，可能反而沒有聲音。某些村里可能同時具備高淹水或土石流風險、高齡人口比例高、道路受阻、通訊不穩或感測器覆蓋不足等條件，卻因為居民無法通報、沒有網路、長者不熟悉數位工具，導致系統看不到它。

因此，第一個元件 **Silent Disaster Zone Detection API（沉默災區偵測 API）** 負責回答：

> 哪些地方「理論上應該需要被注意」，但目前通報很少甚至沒有通報？

找到這些區域後，問題還沒有結束。下一步是：誰要去確認？誰適合搬物資？誰具備醫療能力？誰離現場最近？

因此，第二個元件 **Disaster Volunteer Dispatcher API（救災志工智慧分配 API）** 負責回答：

> 對於這些高優先區域，哪些志工最適合被派去執行確認、巡查或救援任務？

兩個元件合起來，形成一條清楚的防災決策鏈：

```text
沉默災區偵測 API
找出高風險、低通報、低觀測覆蓋的村里
        ↓
產生巡查 / 確認 / 救援任務
        ↓
救災志工智慧分配 API
根據任務類型、志工技能、距離、可用狀態與緊急度產生派遣建議
        ↓
指揮者審核後執行
```

## 2. 元件列表

| 元件 | 功能定位 | 輸入 | 輸出 | 原始 repository |
|---|---|---|---|---|
| Silent Disaster Zone Detection API | 找出高風險但低通報的「沉默災區」 | 村里界、人口、風險圖資、雨量、土石流警戒、路況、通報資料 | `silent_risk.json`、`silent_risk.csv`、`silent_risk.geojson` | [cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api) |
| Disaster Volunteer Dispatcher API | 將任務分配給合適志工 | 任務、志工、技能、位置、可用狀態、緊急度 | 派遣清單、ETA、AI / 演算法推理摘要 | [D4rk-N355/disaster_rescuing](https://github.com/D4rk-N355/disaster_rescuing) |

## 3. repository 結構

```text
disaster-resilience-components/
├── README.md
├── README.en.md
├── docs/
│   ├── story.md
│   ├── story.en.md
│   ├── architecture.md
│   ├── architecture.en.md
│   ├── api_contract.md
│   ├── api_contract.en.md
│   ├── ai_usage.md
│   ├── ai_usage.en.md
│   ├── limitations.md
│   └── limitations.en.md
└── components/
    ├── silent-disaster-zone-api/
    └── disaster_rescuing/
```

> 建議把兩個原本的專案複製到 `components/` 底下，或在 README 中保留原 repo 連結。比起硬合併成一個後端，這樣更能凸顯「積木式元件」的設計。

## 4. 快速理解整合流程

1. **資料進入沉默災區偵測 API**  
   系統整合靜態風險資料與即時事件資料，例如村里界、人口、高齡比例、淹水潛勢、土石流資料、雨量、路況與通報資料。

2. **輸出高優先關注區域**  
   API 輸出村里層級的沉默風險分數、風險等級、原因說明與 GeoJSON 圖層。

3. **轉換成巡查或救援任務**  
   高風險但低通報的區域可以轉成任務，例如「請確認道路是否可通行」、「請確認弱勢住戶狀況」、「請確認是否有物資需求」。

4. **送入志工智慧分配 API**  
   Dispatcher API 根據任務類型、志工技能、志工位置、可用狀態與緊急度，輸出建議派遣結果。

5. **人類指揮者做最後決策**  
   AI 與演算法只提供建議，不自動發布撤離命令，不取代政府或現場指揮權責。

## 5. 文件導覽

| 文件 | 中文 | English |
|---|---|---|
| 故事與問題定義 | [docs/story.md](docs/story.md) | [docs/story.en.md](docs/story.en.md) |
| 系統架構 | [docs/architecture.md](docs/architecture.md) | [docs/architecture.en.md](docs/architecture.en.md) |
| API 契約 | [docs/api_contract.md](docs/api_contract.md) | [docs/api_contract.en.md](docs/api_contract.en.md) |
| AI 使用說明 | [docs/ai_usage.md](docs/ai_usage.md) | [docs/ai_usage.en.md](docs/ai_usage.en.md) |
| 限制與風險 | [docs/limitations.md](docs/limitations.md) | [docs/limitations.en.md](docs/limitations.en.md) |
| 資料來源與接入規劃 | [docs/data_sources.md](docs/data_sources.md) | [docs/data_sources.en.md](docs/data_sources.en.md) |

## 6. MVP 範圍

目前 MVP 聚焦於：

- 花蓮縣村里層級的沉默災區偵測
- 村里風險分數與 GeoJSON 圖層輸出
- 任務與志工資料的標準化 JSON 輸入
- Ollama 本地 AI 派遣建議
- AI 失敗時的本地演算法保底派遣
- FastAPI / Swagger 文件展示

## 7. 核心價值

本作品的重點不是「做一套包山包海的平台」，而是把災害應變流程拆成兩個清楚、可重複使用的積木：

1. **看見被忽略的地方**：避免只關注通報量高的熱區，而漏掉高風險但沉默的區域。
2. **把人派到需要的地方**：讓確認、巡查、搬運、醫療、行政等任務能更快找到合適人力。

## 8. 使用界線

本專案輸出的分數與派遣結果都是**決策輔助資訊**，不是最終災情判定，也不是正式撤離命令。正式應變仍應由具權責的政府單位、現場指揮者或專業人員確認。
