# GCP 課堂筆記（2025/11/02 下午）

## 課程焦點

-   介紹 GCP 托管式資料服務：Cloud SQL、Cloud Storage（GCS）、BigQuery。
-   透過成本與維運比較，說明何時選擇託管服務、何時自行建置 VM。
-   演練從 GCS 上傳檔案、連結 BigQuery 建立資料表並進行查詢的完整流程。

------------------------------------------------------------------------

## Cloud SQL 服務概述

-   Cloud SQL 提供 MySQL、PostgreSQL、SQL Server 三種主流資料庫，專注於讓使用者免維護底層主機。
-   建立資料庫時需選擇方案（Enterprise Plus/Enterprise）、機器規格與磁碟類型，右側會即時顯示每小時費用。
-   預設會啟用自動備份與跨區域儲存，成本較自建 VM 高，適合正式環境或對備援要求高的情境。
-   若僅需練習，可改用 Compute Engine + Docker 起 MySQL，省下託管服務費用並保留環境掌控度。

------------------------------------------------------------------------

## Cloud Storage（GCS）操作

-   GCS Bucket 適合保存結構化／非結構化檔案，可透過 Console、`gsutil` 或應用程式 API 互動。
-   示範建立 Bucket、設定區域與儲存類別，並上傳課程資料夾以模擬原始資料上雲。
-   說明 ACL／IAM 權限配置：若從 VM 操作 GCS，需替該 VM 使用的服務帳戶賦予 Storage 權限。
-   與 AWS S3、Azure Blob 的 UI 與概念類似，轉換雲端平台時只需調整連線端點與授權。

------------------------------------------------------------------------

## BigQuery 與資料匯入

-   BigQuery 支援從 GCS、Google Sheets 等來源匯入資料；課堂示範由 GCS 選取檔案建立外部資料表。
-   建立 Dataset 後可透過 UI 指定 Schema、分割設定或選擇外掛表（External Table）直接指向 GCS。
-   查詢語法與標準 SQL 類似，但 BigQuery 有額外的函式與費用計算方式；執行查詢會顯示掃描資料量。
-   建議在建立測試表前先確認檔案格式（CSV、Parquet 等），必要時可先在本機或 Notebook 轉換格式。

------------------------------------------------------------------------

## 權限與費用控管

-   使用服務帳戶時可套用細粒度角色（如 Storage Object Admin、BigQuery Data Viewer），避免給予過大權限。
-   刪除不再使用的 Cloud SQL、Bucket、BigQuery Dataset，以免額度快速耗盡；Spot VM 或停用資源也能節省成本。
-   若要排程資料搬運到 GCS 或 BigQuery，可結合 Airflow、Cloud Functions 或定期執行的 VM 腳本。

------------------------------------------------------------------------

## 參考來源

-   原始逐字稿：tmp/Tibame 20251102 gcp afternoon.txt

