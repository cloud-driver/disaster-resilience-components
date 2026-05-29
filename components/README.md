<p align="right">
繁體中文 | <a href="./README.en.md">English</a>
</p>

# Components

本資料夾保存兩個防災元件的本地快照，方便評審 clone 主 repo 後可以看到完整交件結構。  
但請注意：**兩個元件的主要審查入口仍然是原始 repository。**

---

## 原始元件 Repository

| 元件 | 原始 repository | 功能 |
|---|---|---|
| 沉默災區偵測 API | [cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api) | 找出高風險但低通報的區域，輸出 JSON / CSV / GeoJSON |
| 救災志工智慧分配 API | [D4rk-N355/disaster_rescuing](https://github.com/D4rk-N355/disaster_rescuing) | 根據任務需求、志工技能、位置與可用狀態產生派遣建議 |

---

## 建議審查路線

```text
1. 先看原始元件 repo：Silent Disaster Zone Detection API
        ↓
2. 再看原始元件 repo：Disaster Volunteer Dispatcher API
        ↓
3. 回到主 repo，執行 examples/integration_demo.py
        ↓
4. 查看 schemas/、openapi/ 與 docs/，確認資料交換與整合設計
```

---

## 為什麼保留本地快照？

本地快照的目的不是取代原始 repo，而是讓主 repo 在 clone 後具備完整交件脈絡。

它可以幫助評審快速理解：

1. 本作品確實由兩個元件組成
2. 兩個元件可以獨立存在
3. 主 repo 只是整合入口與展示層
4. 整合 demo 如何將兩個元件串接起來

---

## 本地資料夾說明

```text
components/
├── README.md
├── README.en.md
├── silent-disaster-zone-api/
└── disaster-rescuing/
```

| 資料夾 | 說明 |
|---|---|
| `silent-disaster-zone-api/` | 沉默災區偵測元件的本地快照 |
| `disaster-rescuing/` | 救災志工智慧分配元件的本地快照 |

---

## 與主 repo 的關係

主 repo 的整合 demo 位於：

```text
examples/integration_demo.py
```

整合 demo 會模擬以下流程：

```text
沉默災區偵測結果
        ↓
IntegratedTask 標準任務格式
        ↓
志工分配邏輯
        ↓
派遣建議
```

其中 `IntegratedTask` 的資料格式定義於：

```text
schemas/integrated_task.schema.json
```

整合流程的 OpenAPI 契約定義於：

```text
openapi/integrated-flow-api.yaml
```

---

## 更新本地快照的方式

若需要更新本地快照，請從原始 repo 重新同步。  
更新前請確認不會帶入 `.env`、token、API key、真實個資或私人 IP。

範例流程：

```bash
rm -rf components/silent-disaster-zone-api
rm -rf components/disaster-rescuing

git clone https://github.com/cloud-driver/silent-disaster-zone-api.git /tmp/silent-disaster-zone-api
git clone https://github.com/D4rk-N355/disaster_rescuing.git /tmp/disaster-rescuing

cp -R /tmp/silent-disaster-zone-api components/silent-disaster-zone-api
cp -R /tmp/disaster-rescuing components/disaster-rescuing

rm -rf components/silent-disaster-zone-api/.git
rm -rf components/disaster-rescuing/.git
```

---

## 不應放入本資料夾的內容

請勿將以下內容 commit 到本資料夾：

- `.env`
- API key
- token
- 密碼
- 真實志工個資
- 真實聯絡方式
- 私人 IP
- Tailscale IP
- ngrok URL
- `__pycache__/`
- `.DS_Store`

本資料夾只應保留可以公開審查的程式碼、文件、樣本資料與元件說明。