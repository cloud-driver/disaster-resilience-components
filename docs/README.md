<p align="right">
繁體中文 | <a href="./README.en.md">English</a>
</p>

# 整合文件導覽

本資料夾說明母 repo 如何把「沉默災區偵測」與「志工派工」兩個獨立元件放在同一條可審查的決策鏈中。

## 建議閱讀順序

1. [快速開始](./quickstart.md)：先跑離線樣本 demo，再選擇啟動兩個上游元件。
2. [故事與情境](./story.md)：理解要補的是何種資訊缺口。
3. [系統架構](./architecture.md)：確認元件邊界與目前整合程度。
4. [流程圖](./diagrams.md)：查看資料流、雙隊列、人工覆核位置。
5. [API 與資料契約](./api_contract.md)：查看真實 API、`IntegratedTask` 與 adapter。
6. [資料來源](./data_sources.md)：確認資料模式、可信度與限制。
7. [AI 使用](./ai_usage.md) 與 [AI 治理](./ai_governance.md)：確認 AI 不能越過的責任界線。
8. [限制與後續](./limitations.md)：確認 MVP 還沒做到什麼。

## 最重要的現況聲明

- 本 repo 的 `examples/integration_demo.py` 是以樣本 JSON 驗證資料轉換與候選排序的**離線 demo**。
- `openapi/integrated-flow-api.yaml` 是一份**目標整合契約**；它不是目前部署中的 HTTP endpoint。
- 沉默元件與志工元件可各自啟動，但正式跨服務串接仍需 adapter，將 `IntegratedTask` 轉成志工元件的 `DispatchRequest`。
- 不可把 sample、batch 或未驗證通報，說成即時災情或自動救援結果。

回到：[母 repo 首頁](../README.md)。
