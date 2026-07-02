# 交件與展示檢查表

此清單用於確認本 repo 的文件陳述與程式現況一致。不要為了讓作品看起來完整而寫入無法證明的能力。

## 文件一致性

- [ ] 原始志工派工 repo 連結為 `https://github.com/D4rk-N355/volunteer_distributing`。
- [ ] 任何提及 `components/disaster-rescuing/` 的地方都說明它是**本地快照的歷史資料夾名稱**。
- [ ] 明確區分「本 repo 的離線樣本整合 demo」與「尚待建置的正式 API-to-API adapter」。
- [ ] `openapi/integrated-flow-api.yaml` 被描述為**目標整合契約／facade 規格**，不是目前已部署 endpoint。
- [ ] 所有 API 文件都以子 repo 當前 Swagger／原始碼為準；不要使用過時的 snapshot 文件覆蓋實作現況。

## 可行性與 MVP

- [ ] `python3 examples/integration_demo.py` 可執行並產生 `examples/sample_dispatch_output.json`。
- [ ] demo 能展示風險資料、任務化、候選志工、重複指派避免與警示。
- [ ] 說明 sample 資料只用於資料流驗證，不能被稱為即時災情。
- [ ] 說明沉默元件目前的 MVP 分析單位為花蓮縣村里層級。
- [ ] 說明志工派工服務的活動設定與報名資料目前會保存在記憶體中，服務重啟後消失。

## Input / Process / Output

- [ ] 清楚列出沉默元件的輸入、規則式處理、JSON / CSV / GeoJSON 輸出與 metadata。
- [ ] 說明 `pending → verified / rejected` 通報生命週期。
- [ ] 說明 `silent_watch_queue` 與 `verified_incident_queue` 的不同用途。
- [ ] 提供 `schemas/integrated_task.schema.json` 連結。
- [ ] 說明正式 adapter 需將 `IntegratedTask` 轉換為志工服務的 `DispatchRequest`，不是直接把兩種 schema 視為相容。

## AI 與責任邊界

- [ ] 不說「預測災害」、「自動救災」或「保證被救援」。
- [ ] 明確寫出：`silent_risk_score` 是人工確認優先序，不代表災害已發生。
- [ ] 明確寫出：沉默元件的 Ollama 僅整理已存在的規則式結果，不能改變排序或發布命令。
- [ ] 明確寫出：志工元件的 Ollama 僅做選用異常檢查；不可取代核心 deterministic dispatch。
- [ ] 任何派工結果都保留給人員／指揮單位最終覆核。

## 資安、個資與展示

- [ ] `.env`、API key、管理金鑰、密碼 hash 與 token 不存在於 repo。
- [ ] LINE 回報原始 user ID 不直接存入正式通報資料；以 HMAC／雜湊方式處理。
- [ ] 正式對外部署時，沉默元件使用 HTTPS、反向代理與合理的 token／admin-key 管理。
- [ ] 志工派工 API 若要公開使用，額外加上反向代理、存取控制、HTTPS、限流與稽核，因其目前文件未定義完整對外授權模型。
- [ ] 簡報與 README 的日期、API 路徑、repo 連結、圖表和實際畫面一致。
