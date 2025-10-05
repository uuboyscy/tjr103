# Data Pipeline 課堂筆記（2025/10/03 下午）

## Dev Container 快速複習

-   啟動流程：安裝 Dev Containers 擴充套件、確認 Docker 運作、專案根目錄放置 `.devcontainer/`，再以 Command Palette 重新開啟容器。
-   若建置卡住，刪除對應 image / container 後重啟 VS Code，再從啟動步驟重新執行。
-   `devcontainer.json` 為核心設定檔，負責指定映像檔、擴充套件與啟動時需要執行的指令。

------------------------------------------------------------------------

## 課程主題與規劃

-   資料管線課程將帶入：Pandas 資料處理、資料庫連線、利用 Airflow 監控與排程 Pipeline。
-   強調建立一致的 Python 環境是後續練習（資料庫、ETL、自動化）順利的基礎。

------------------------------------------------------------------------

## Poetry 與 pipx 的安裝策略

-   推薦使用 Poetry 管理專案依賴與虛擬環境，取代傳統 `pip` + `requirements.txt`。
-   Poetry 官方建議透過 `pipx` 安裝：`pipx` 會為每個 CLI 工具提供獨立的 Python 環境，避免汙染系統或專案。
-   Windows：以官方提供的 PowerShell 指令直接安裝。
-   macOS：先裝 Homebrew，再用 Homebrew 裝 `pipx`，最後以 `pipx install poetry` 完成；`pipx` 也適用於 Windows 但步驟較繁瑣。

------------------------------------------------------------------------

## Markdown 與筆記習慣

-   示範使用 Markdown 撰寫課堂筆記，包含標題層級、清單與表格，方便轉換為 GitHub 文件。
-   鼓勵將課堂示範的命令與說明記錄於專案 README，方便同學事後複習。

------------------------------------------------------------------------

## 在 VS Code 使用 Jupyter Notebook

-   安裝 VS Code 的 Jupyter 擴充套件後，新建 `.ipynb` 檔案即可撰寫互動式程式。
-   首次開啟需選擇 Kernel，建議挑選 Poetry 建立的虛擬環境；若選單仍顯示 `Select Kernel`，可重新載入視窗或手動指定。
-   若執行 cell 時出現紅字錯誤，代表缺少 Jupyter 內核，可執行 `poetry add jupyter` 以 Poetry 安裝套件。
-   說明 Jupyter 架構：VS Code 擴充套件負責前端介面，`jupyter` / `ipython` 套件提供後端執行引擎。

------------------------------------------------------------------------

## Pandas 入門

-   透過 Notebook 匯入 `pandas as pd`、`numpy as np`，練習建立資料表與顯示結果。
-   說明 DataFrame 的欄位在 Notebook 中會以表格形式渲染，比傳統終端輸出更易閱讀。
-   後續晚間課程將延續此環境，進一步操作欄位增刪、索引與資料組合。
