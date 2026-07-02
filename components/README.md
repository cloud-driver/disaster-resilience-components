<p align="right">
繁體中文 | <a href="./README.en.md">English</a>
</p>

# 元件快照導覽

此資料夾保存兩個防災元件的**本地審閱快照**，讓評審即使只 clone 母 repo，也能閱讀核心程式、樣本資料與文件。快照不是 submodule，也不會自動與上游同步；發現衝突時，應以上游原始 repository 的當前程式與 Swagger 文件為準。

| 本地快照 | 上游實作來源 | 元件定位 | 目前應注意的事實 |
|---|---|---|---|
| [`silent-disaster-zone-api/`](./silent-disaster-zone-api/) | [cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api) | 高風險、低觀測、低通報區域辨識；LINE 回報、人工查證、已驗證事件與指揮建議。 | 正式排序為可解釋的規則式邏輯；AI 僅做受限制摘要。 |
| [`disaster-rescuing/`](./disaster-rescuing/) | [D4rk-N355/volunteer_distributing](https://github.com/D4rk-N355/volunteer_distributing) | 依任務、技能、距離、可用性產生志工候選與派工建議。 | 本地資料夾保留歷史名稱；上游 repo 名稱已是 `volunteer_distributing`。 |

## 版本與審閱原則

1. **上游為實作真相來源。**母 repo 的 snapshot 用於展示與整合閱讀；實際 endpoint、環境變數與安全機制應回到上游 README、Swagger 或程式碼確認。
2. **不把文件當成服務已部署的證據。**母 repo 的 `examples/integration_demo.py` 是樣本資料的離線驗證，不是 API-to-API 連線測試。
3. **保留現況差異。**`IntegratedTask` 是母 repo 的正規化交換格式；志工服務現有 API 使用 `DispatchRequest`。兩者需由 adapter 轉換，不能直接假設 JSON 完全相容。
4. **不得上傳敏感資料。**快照與上游皆不得包含 `.env`、token、API key、LINE user ID、未去識別通報內容或個資。

## 建議閱讀順序

```text
1. silent-disaster-zone-api/README.md
2. disaster-rescuing/README.md
3. ../docs/api_contract.md
4. ../examples/integration_demo.py
5. ../schemas/integrated_task.schema.json
```

回到母 repo：[整合文件首頁](../README.md)。
