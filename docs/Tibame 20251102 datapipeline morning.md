# Data Pipeline 課堂筆記（2025/11/02 上午）

## 課程焦點

-   將前一天手動部署 Airflow 的流程轉換為可重複的啟動腳本（startup script）。
-   學習在 VM 啟動時自動安裝套件、建立使用者、抓取程式碼並啟動服務。
-   認識 root 與一般使用者權限的區分，避免腳本因權限不足而失敗。

------------------------------------------------------------------------

## Startup Script 基本結構

-   腳本以 `#!/bin/bash` 開頭，GCE 會以 root 權限執行；適合處理系統層級的安裝與設定。
-   常見前置步驟：`apt-get update -y` 更新套件索引、安裝 `docker.io`、`git` 等必要工具。
-   可搭配 `sleep` 確保服務啟動有足夠時間，再執行後續指令（例如建立 Airflow 使用者）。
-   建議先在本機文字檔編輯腳本，再貼到 Console 的 metadata 或 `gcloud` 指令避免輸入錯誤。

------------------------------------------------------------------------

## 使用者與權限配置

-   以 `useradd -m tjr103-gcp-user` 建立專用帳號，並設定家目錄作為專案根目錄。
-   透過 `usermod -aG docker` 將帳號加入 docker 群組，避免以 root 身份操作容器。
-   掛載目錄需要跨容器存取時，可先 `chmod -R 777 airflow-demo` 或依需求調整為更精細的權限。
-   `git config --global --add safe.directory <path>` 與 `git config core.filemode false` 可避免因權限變更造成 Git 告警。

------------------------------------------------------------------------

## 自動佈署 Airflow

-   腳本在使用者家目錄執行 `git clone https://github.com/uuboyscy/airflow-demo.git` 取得課程專案。
-   以 `docker run -it -d --name airflow-server ... apache/airflow:2.11.0-python3.12 airflow standalone` 啟動容器，掛載 `dags`、`logs`、`utils`、`tasks`。
-   加入 `sleep 15` 等待服務啟動，再用 `docker exec airflow-server airflow users create ...` 建立預設管理者帳號。
-   腳本結束後即可直接透過瀏覽器訪問 Airflow UI，不需手動登入主機。

------------------------------------------------------------------------

## gcloud 指令與參數說明

-   `gcloud compute instances create` 可透過 `--metadata startup-script='...'` 將上述腳本內嵌於指令。
-   示範同時建立標準（`--provisioning-model=STANDARD`）與 Spot VM（`--provisioning-model=SPOT`），說明費用與中斷行為差異。
-   參數中包含 `--tags`（控制防火牆套用）、`--scopes`（授權 API 存取）、`--create-disk`（指定開機磁碟規格）等常見設定。
-   提醒部署大量參數時善用換行與 `\` 或 `$'\n'` 格式，確保指令在 Shell 中正確解析。

------------------------------------------------------------------------

## 參考來源

-   原始逐字稿：tmp/Tibame 20251102 datapipeline morning.txt

