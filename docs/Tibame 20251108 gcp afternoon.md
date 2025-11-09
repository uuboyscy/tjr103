# GCP 課堂筆記（2025/11/08 下午）

## 課程焦點

-   延伸上午的 `pygsheets` 範例，示範將 pandas DataFrame 上傳到新 Sheet、同步成 BigQuery 外部來源。
-   介紹 Secret Manager：建立 Secret、版本輪替、程式端讀取與權限控管。
-   建立 Artifact Registry 以及服務帳戶，完成 Docker Login、建置多架構映像並推送。
-   系統化拆解 Cloud Run 的 Service / Job / Function，說明典型情境與部署細節，並與 Airflow 等排程工具整合。

------------------------------------------------------------------------

## pygsheets 進階應用

-   同一份 Google Sheet 可新增額外工作表專門存放程式寫入結果，避免覆寫原本給同仁填寫的頁籤。
-   實作 `worksheet.set_dataframe(df, (1, 1))`、`worksheet.update_values()` 等方法，確認 DataFrame 欄位順序與標題一次寫入。
-   若要讓 BigQuery 外部表指向新的頁籤，記得更新 `Sheet range` 並保留第一列作為標題列。

------------------------------------------------------------------------

## Secret Manager 實務

-   Console 建立 Secret 時，可選擇手動輸入字串或上傳 JSON（金鑰、設定檔等）；系統自動產生版本號管理歷史值。
-   建議依專案或服務拆分 Secret（例如 `bigquery-user`, `artifact-registry-user`），也能針對同一 Secret 開多個版本並視需要 disable 舊版。
-   程式端示範建立 `secretmanager.SecretManagerServiceClient()`，透過 `projects/<id>/secrets/<name>/versions/latest` 讀取，加上 `poetry add google-cloud-secret-manager`.
-   將下載的 JSON 金鑰寫入 Secret 後，本地檔案加進 `.gitignore`；Notebook 內以環境變數或暫存檔方式載入，避免留在版本控制。

------------------------------------------------------------------------

## Artifact Registry 與容器映像

-   建立地區型 Artifact Registry（例：`asia-east1`），命名規則為 `asia-east1-docker.pkg.dev/<project>/<repo>/<image>:tag`。
-   新增 `artifact-registry-user` Service Account，授予 `Artifact Registry Administrator` 或針對特定 repo 的寫入權限。
-   Docker 登入指令：
    -   macOS/Linux：`cat artifact-registry-user.json | docker login -u _json_key --password-stdin https://asia-east1-docker.pkg.dev`
    -   Windows PowerShell 使用 `Get-Content -Raw`.
-   示範 Dockerfile：以 `python:3.11-slim` 建置 Flask sample，安裝 zsh/Oh My Zsh、pip 套件，最後 `CMD ["flask", "run"]`。
-   在 M-series Mac 需要 `docker build --platform=linux/amd64 ...` 以符合 Cloud Run 僅支援 x86_64 的限制；推送前確認標籤一致。

------------------------------------------------------------------------

## Cloud Run（Service / Job / Function）

-   Cloud Run Service：長時常駐 HTTP 容器，適合 REST API、Webhook；部署時需指定映像、區域、執行個體資源、同時處理數量以及是否允許未授權調用。
-   Cloud Run Job：一次性或批次作業，可設定執行次數與併行度；常透過 Cloud Scheduler、Airflow Cloud Run Job Operator 觸發，適合 ETL 或資料整理腳本。
-   Cloud Run Function：事件驅動輕量函式，背後仍由 Cloud Run 承載，但開發體驗接近 Functions，適合 Pub/Sub 或 Storage 觸發。
-   Artifact Registry 映像與 Cloud Run 綁定時，要確保部署服務帳戶具有 `Artifact Registry Reader`、`Cloud Run Invoker` 等必要權限。
-   透過 Infrastructure as Code（如 Terraform）或 GCP Console 都能設定環境變數、VPC 連線、最小最大執行個體，課堂亦提到以 Airflow Operator 觸發 Cloud Run 任務的做法。

------------------------------------------------------------------------

## 參考來源

-   原始逐字稿：tmp/Tibame 20251108 gcp afternoon.txt

