# GCP 課堂筆記（2025/11/08 上午）

## 課程焦點

-   在 BigQuery 建立指向 Google Sheet 的 External Table，示範設定資料來源、欄位範圍與 Schema。
-   透過 Poetry + `google-cloud-bigquery` 建立 Notebook，練習以程式查詢 BigQuery 並輸出成 pandas DataFrame。
-   建立專用 Service Account，處理 BigQuery、GCS、Google Drive/Sheet 的授權與憑證載入方式。
-   介紹 `pygsheets` 套件，示範如何讀寫 Sheet、同步 DataFrame，以及將更新回寫成外部資料來源。

------------------------------------------------------------------------

## Google Sheet External Table 流程

-   在建立資料表時，來源選擇 `Drive` 並貼上 Google Sheet 連結；建議移除網址 query 參數避免授權疑慮。
-   `File format` 選 `Google Sheet`，`Sheet range` 使用 `工作表名稱!A:D` 這類寫法，直接用欄位字母定義整欄，才能自動吃到後續新增列。
-   Schema 可以在「Edit as text」貼上事先整理好的 JSON，例如 `[{ "name": "store_id", "type": "STRING" }, ...]`；記得 `Header rows to skip` 設為 1。
-   建立完成後即可在 BigQuery UI 直接 Query，唯有讀取權限，寫入需要回到原來源（例如 Sheet 或 GCS）處理。

------------------------------------------------------------------------

## Python 版 BigQuery Client 實作

-   使用 `poetry init` 建專案後，安裝 `google-cloud-bigquery pandas db-dtypes`，並以 Jupyter/Colab Notebook 示範。
-   建議先以 `Credentials.from_service_account_file(..., scopes=[...])` 產生憑證，再 `client = bigquery.Client(project=..., credentials=...)`。
-   以 `client.query(SQL).result().to_dataframe()` 取得結果，示範 DataFrame 轉 dict / list 以供後續寫 GCS、呼叫 API 或建立報表。
-   若查詢的 External Table 連到 Google Drive 或 GCS，程式端要確保對應 scope (`cloud-platform`, `bigquery`, `drive`) 都授權。

------------------------------------------------------------------------

## 憑證與權限實務

-   練習建立 `bigquery-user` Service Account：至少給 `BigQuery Data Viewer` + `BigQuery Job User`，需要讀 GCS 時再加 `Storage Object Admin`。
-   下載 JSON Key 後可：
    -   直接在程式載入檔案。
    -   設定 `export GOOGLE_APPLICATION_CREDENTIALS=<path>` 供 SDK 自動抓取。
-   Google Sheet 需與該 Service Account 分享（Editor 權限），否則會遇到 `Drive API` 或 `GCS` 權限不足錯誤。
-   測試權限時可先給較寬鬆角色確認流程可跑，再逐步收斂權限，避免卡在授權問題。

------------------------------------------------------------------------

## 使用 pygsheets 操作 Google Sheet

-   課堂示範安裝 `pygsheets`，以同一把服務帳戶金鑰授權，呼叫 `pygsheets.authorize(service_file=...)`。
-   `client.open_by_url(sheet_url)` 取到 Sheet 後，可用 `worksheet = sh.worksheet_by_title("Sheet1")` 指定工作表。
-   讀取資料時可 `worksheet.get_as_df(has_header=True)` 直接轉成 pandas DataFrame；寫入則示範 `set_dataframe(df, (1,1))` 與 `update_values`。
-   實務上建議透過 API / pygsheets 修改外部資料來源，再讓 BigQuery 外部表讀取，避免直接嘗試在 BigQuery UI 改外部表內容。

------------------------------------------------------------------------

## 參考來源

-   原始逐字稿：tmp/Tibame 20251108 gcp morning.txt

