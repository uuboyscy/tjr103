# Docker 課堂筆記（2025/10/03 上午）

## Dev Container 與 VS Code 整合

-   使用 VS Code 的 Dev Container 功能，直接在容器內開發並共享一致的環境。
-   連線模式分為遠端實體機與本地 Docker 容器，課堂聚焦後者。
-   操作流程：下載示範專案（含 `.devcontainer`），在 VS Code 開啟資料夾、安裝 Dev Containers 擴充套件、確認 Docker 已啟動，最後透過 Command Palette (`⇧⌘P / ⇧Ctrl+P`) 執行 `Dev Containers: Reopen in Container`。

------------------------------------------------------------------------

## 專案結構與設定檔

-   專案根目錄需包含 `.devcontainer/`，內放 `devcontainer.json` 與自訂 `Dockerfile`。
-   `devcontainer.json` 主要用途：指定基底影像來源、掛載與執行參數、安裝常用 VS Code 擴充套件（Python、格式化、Git 工具等）、預設編輯器樣式（ruler、tab 寬度）以及啟動後要執行的指令。
-   若開啟容器過程卡住，可刪除對應的 image / container 後重新透過 Command Palette 啟動。

------------------------------------------------------------------------

## Dockerfile 重點

-   由官方 Python image 建立，課程示範會：設定時區為台北、複製 `requirements.txt` 進容器、以 `apt-get` 安裝 Git、Zsh、Vim 等工具。
-   透過 `pip install -r requirements.txt` 安裝基礎套件，但講師提醒：僅作為示範，實務上會選擇更完善的環境管理方案。\\
-   Dev Container 啟動時會先建置 image、再依序執行 `postCreateCommand` 安裝依賴與擴充套件。

------------------------------------------------------------------------

## Python 套件管理建議

-   `requirements.txt` 雖常見，但難以追蹤相依版本與來源。
-   推薦改用 Poetry：支援虛擬環境隔離、相依版本求解、產生 `poetry.lock` 與套件來源雜湊，降低供應鏈風險。
-   下午的資料管線課程會示範以 Poetry 初始化專案並管理套件，取代傳統 `pip` 與 `requirements.txt` 的流程。
