<p align="right">
繁體中文 | <a href="./README.en.md">English</a>
</p>

# 文件導覽
本資料夾整理 **Disaster Resilience Components** 的設計文件、技術規格與審查導覽。
本作品由 **Islewise Tech** 製作，目標是以「積木式設計」建立可重複使用、可獨立運作、可與其他系統整合的防災 API 元件。

本主儲存庫整合兩個核心元件：

1. **Silent Disaster Zone API**
   偵測「高風險但低通報」的沉默災區，輸出需要主動查核的區域。

2. **Volunteer Dispatch API**
   根據任務需求、志工技能、位置與可用狀態，推薦合適的救災志工。

兩個元件可獨立使用，也可串接成一條防災決策輔助流程：

```text
公開風險資料 / 通報資料 / 道路狀態 / 村里資料
        ↓
Silent Disaster Zone API
        ↓
高風險低通報區域
        ↓
任務轉換
        ↓
Volunteer Dispatch API
        ↓
推薦志工與派遣建議
```

---

## 評審快速閱讀路徑

若時間有限，建議依照下列順序閱讀：

| 順序 | 文件 / 目錄                                                                            | 用途                                   |
| -- | ---------------------------------------------------------------------------------- | ------------------------------------ |
| 1  | [`../README.md`](../README.md)                                                     | 了解作品問題、解法、元件組合與整體價值                  |
| 2  | [`quickstart.md`](./quickstart.md)                                                 | 快速執行 MVP demo                        |
| 3  | [`diagrams.md`](./diagrams.md)                                                     | 查看系統流程、資料流與元件邊界                      |
| 4  | [`architecture.md`](./architecture.md)                                             | 了解整體架構、模組分工與整合方式                     |
| 5  | [`api_contract.md`](./api_contract.md)                                             | 查看 Input / Process / Output 與 API 契約 |
| 6  | [`../schemas/integrated_task.schema.json`](../schemas/integrated_task.schema.json) | 查看整合任務的 JSON Schema                  |
| 7  | [`../openapi/integrated-flow-api.yaml`](../openapi/integrated-flow-api.yaml)       | 查看 OpenAPI / Swagger 規格              |
| 8  | [`data_sources.md`](./data_sources.md)                                             | 查看可串接的真實防災資料來源                       |
| 9  | [`ai_usage.md`](./ai_usage.md)                                                     | 了解 AI 在作品中的角色與使用方式                   |
| 10 | [`ai_governance.md`](./ai_governance.md)                                           | 查看 AI 風險、限制、人機協作與治理原則                |
| 11 | [`../components/README.md`](../components/README.md)                               | 查看兩個子元件的導覽與原始專案連結                    |
| 12 | [`../examples/integration_demo.py`](../examples/integration_demo.py)               | 查看可執行的整合示範程式                         |

---

## 文件列表

### [`quickstart.md`](./quickstart.md)

提供最短路徑的執行方式，用於驗證本作品的 MVP 資料流。

重點包含：

* 如何執行整合 demo
* demo 的輸入與輸出
* 如何確認兩個元件的串接邏輯
* 如何理解 sample data 與實際部署資料的差異

---

### [`architecture.md`](./architecture.md)

說明本作品的整體技術架構與元件邊界。

重點包含：

* 雙元件架構
* 元件責任分工
* 資料流設計
* 可獨立部署與可整合使用的方式
* 未來串接外部防災系統的可能性

---

### [`diagrams.md`](./diagrams.md)

提供流程圖與系統圖，協助快速理解作品運作方式。

重點包含：

* 系統整體流程
* 元件間資料流
* Silent Disaster Zone API 到 Volunteer Dispatch API 的轉換流程
* 人機協作與人工審核節點

---

### [`api_contract.md`](./api_contract.md)

定義兩個元件與整合流程的 API 契約。

重點包含：

* Endpoint 說明
* Request / Response 格式
* Input / Process / Output 定義
* 元件之間的資料交換方式
* 標準化 JSON 資料格式

---

### [`data_sources.md`](./data_sources.md)

說明本作品在正式部署時可串接的真實防災資料來源。

重點包含：

* 災害風險資料
* 村里與人口資料
* 道路中斷與交通資料
* 災情通報資料
* 志工與資源資料
* 授權、隱私與資料品質限制

本作品的 demo 使用 sample / mock data 來驗證流程；正式部署時可依此文件替換為真實開放資料或授權資料來源。

---

### [`ai_usage.md`](./ai_usage.md)

說明 AI 在本作品中的角色。

重點包含：

* AI 如何輔助風險分析
* AI 如何輔助任務摘要與派遣建議
* AI 不負責最終決策
* AI 輸出如何被限制在可審核、可追蹤的範圍內
* 使用生成式 AI 輔助設計與開發的方式

---

### [`ai_governance.md`](./ai_governance.md)

說明 AI 使用邊界、潛在風險與治理原則。

重點包含：

* 不由 AI 自動發布撤離命令
* 不由 AI 自動決定災害等級
* 不由 AI 自動執行派遣命令
* 保留人工審核與人工覆核
* 資料不足、模型不確定或服務失效時的 fallback 原則
* 防止錯誤建議、過度自動化與誤用的設計

---

## 規格與程式碼位置

| 類型          | 路徑                                                                   | 說明                            |
| ----------- | -------------------------------------------------------------------- | ----------------------------- |
| 整合 demo     | [`../examples/integration_demo.py`](../examples/integration_demo.py) | 可直接執行的 MVP 串接示範               |
| 範例輸入資料      | [`../examples/sample_input/`](../examples/sample_input/)             | demo 使用的 sample input         |
| 範例輸出資料      | [`../examples/sample_output/`](../examples/sample_output/)           | demo 產生或參考的 sample output     |
| JSON Schema | [`../schemas/`](../schemas/)                                         | 標準化資料交換格式                     |
| OpenAPI 規格  | [`../openapi/`](../openapi/)                                         | API 型元件的 Swagger / OpenAPI 契約 |
| 元件目錄        | [`../components/`](../components/)                                   | 兩個防災元件的導覽與子專案連結               |

---

## 與競賽要求的對應

| 競賽要求                     | 對應位置                                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| GitHub 專案連結              | [`../README.md`](../README.md)                                                                                           |
| 元件功能定位與欲解決問題             | [`../README.md`](../README.md), [`architecture.md`](./architecture.md)                                                   |
| Input / Process / Output | [`api_contract.md`](./api_contract.md)                                                                                   |
| JSON Schema              | [`../schemas/integrated_task.schema.json`](../schemas/integrated_task.schema.json)                                       |
| 使用流程或系統架構圖               | [`diagrams.md`](./diagrams.md), [`architecture.md`](./architecture.md)                                                   |
| AI 技術架構與使用說明             | [`ai_usage.md`](./ai_usage.md)                                                                                           |
| AI 潛在風險與使用限制             | [`ai_governance.md`](./ai_governance.md)                                                                                 |
| 真實防災資料來源                 | [`data_sources.md`](./data_sources.md)                                                                                   |
| Client sample code       | [`../examples/integration_demo.py`](../examples/integration_demo.py)                                                     |
| README 指引與依賴環境說明         | [`../README.md`](../README.md), [`quickstart.md`](./quickstart.md), [`../components/README.md`](../components/README.md) |
| OpenAPI / Swagger 規格     | [`../openapi/integrated-flow-api.yaml`](../openapi/integrated-flow-api.yaml)                                             |

---

## MVP 驗證方式

在主儲存庫根目錄執行：

```bash
python3 examples/integration_demo.py
```

此 demo 會示範：

1. 接收沉默災區偵測結果
2. 將高風險低通報區域轉換為外勤查核任務
3. 呼叫志工智慧分配邏輯
4. 輸出推薦志工與任務分配結果

此流程可證明兩個元件並非獨立概念，而是可以透過標準化 JSON 資料格式串接成可驗證的防災決策輔助流程。

---

## 注意事項

本作品目前為 MVP 與 prototype 階段，重點在於展示：

* 元件化設計
* 標準化資料交換
* 可驗證的核心流程
* 可擴充的防災資料來源
* AI 輔助但不取代人工決策的治理原則

demo 使用 sample / mock data，不代表正式災害判斷結果。
正式部署時，應串接真實授權資料來源，並由具防災專業的人員進行審核與決策。
