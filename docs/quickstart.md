<p align="right">
繁體中文 | <a href="./quickstart.en.md">English</a>
</p>

# 快速開始

本文件說明如何在本機執行雙元件防災決策鏈的整合 Demo。

## 1. 取得專案

```bash
git clone <your-repository-url>
cd disaster-resilience-components
````

## 2. 確認 Python 版本

建議使用 Python 3.9 以上。

```bash
python3 --version
```

## 3. 執行整合 Demo

```bash
python3 examples/integration_demo.py
```

執行後會看到：

1. 沉默災區偵測結果被轉換成巡查任務
2. 系統根據任務需求與志工資料進行推薦
3. 輸出派遣建議 JSON
4. 產生 `examples/sample_dispatch_output.json`

## 4. Demo 流程

```text
沉默災區偵測 API 輸出
        ↓
高風險低通報區域
        ↓
轉換為巡查 / 救援任務
        ↓
救災志工智慧分配邏輯
        ↓
志工派遣建議
```

## 5. 注意事項

本 Demo 使用樣本資料，不直接代表真實災害派遣結果。
實際部署時，演算法或 AI 推薦結果應由指揮中心、地方政府或現場協調人員進行人工覆核。