# GCP｜Cloud Run Function 與 BigQuery Remote Function（2025/11/22 上午）

## Cloud Run Function 設定要點
- 直接在 Cloud Run（Write Function）建立，區域選台灣、執行環境務必改成 Second Generation（第一代即將淘汰）。
- Runtime 可用 Python 3.13/3.14；部署時先勾 Public access 以便測試，正式版可改為需要 IAM。
- `Entry point` 名稱要與程式中的 handler 同名，否則無法定位入口（範例使用簡單加法函式）。
- 部署後確認 Endpoint 可正常回應，必要時以 `?name=<value>` 帶參數檢查。
- 成本與彈性：請求才起機、可自動水平擴縮，通常比自行維運 VM 更省。

## 串接 BigQuery Remote Function
- 用 Cloud Run Function 作為 Remote Function 的後端，先部署完成並記下 HTTPS URL。
- 在 BigQuery Console 建立連線：`Add data →`（Business application）`Vertex AI / BigQuery federation → Remote Model`，Region 與 dataset 保持一致（台灣）。
- 建立過程會自動產生 Service Account，需賦予 `Cloud Run Invoker`（第二代）權限；若是第一代則給 `Cloud Functions Invoker`。
- Remote Function 設定時要填完整的 Connection ID（含 project/region/connection 名稱）與 Cloud Run URL。
- 練習程式可直接使用官方 sample（函式接受數值做加總），貼上後記得把 handler 名稱同步到 entry point。

## Cloud Run 存取模型的建議
- Cloud Run 容器是短暫磁碟，模型檔應放 GCS；在程式中用具備物件存取權的 Service Account 即時下載。
- 於 Cloud Run 設定執行 Service Account，並賦予必要的 Storage 權限（至少 `Storage Object Viewer` 或讀寫需求對應角色）。

## Prefect 與 Airflow 的差異（課堂補充）
- Prefect（現行免費方案）需透過官方 Work Pool 執行，客製化映像需付費；本地開發可用官方提供的 prebuilt image 加安裝清單。
- Prefect 流程本質是 async I/O，在同一 thread 可看似平行；Airflow 則是 DAG blueprint + multiprocess 執行，新增 DAG 會有渲染延遲。
- Prefect 開發體驗接近一般 Python 腳本（flow/task decorator 後仍可直接執行），但自架 Prefect Server 門檻較 Airflow 稍高。
