# Tibame 20251116 GCP Morning

## Cloud Run Function / Service 現況
- 操作介面改版後，Cloud Run Function 會自動帶入 Google 決定的映像檔與埠號，暫時無法客製，也無法像過去一樣一鍵 Deploy；課堂上實測時官方服務整合中導致整個 Function 失效，只能改用 Cloud Run Service。  
- Service 仍維持原本流程：指定映像檔、CPU/記憶體、同時連線上限與環境變數即可部署，並提供固定的 HTTPS 網址讓所有人共用。  
- 建議先在本機把程式跑穩，再部署到 Service；若後續官方修復 Function，可再把相同的 container 轉回 Function 以便在 BigQuery Remote Function 等服務裡呼叫。

## Selenium 自動化開發流程
- 先在 VS Code 建一個全新的資料夾，透過 `poetry init` 初始化專案並 `poetry add selenium` 安裝驅動；安裝完成後選取 Poetry 建出的虛擬環境作為解譯器。  
- 範例程式存放在講師提供的 GitHub repo (`selenium-demo.py`)，內容示範如何打開 PTT 首頁、點選八卦版、處理 18+ 入口頁，再擷取需要的內容。  
- 透過 Selenium Grid 的 Remote WebDriver 取代 `webdriver.Chrome()`：driver 不再安裝在本機，而是透過 HTTP API 連到遠端 container，程式碼中改成指定 `command_executor` 與 `desired_capabilities`。  
- 操作上盡量改用 `WebDriverWait`/`expected_conditions` 等「顯性等待」來判斷元素是否出現，只有找不到其他判斷方式時才退而求其次使用 `time.sleep()`。  
- 課堂示範腳本會在每一步加上 log，方便之後部署到雲端後比對 Cloud Run 日誌與 Selenium Grid UI（`http://127.0.0.1:4444/ui`）中的 Session 記錄。

## 啟動本機 Selenium Grid
- repo 內附 `run_selenium-grid-chrome-standalone.sh`（Mac/Linux）與對應的 PowerShell 指令（Windows）可直接 `docker run selenium/standalone-chrome`，預設會開啟 `4442/4443/4444` Port。  
- 啟動後瀏覽 `http://localhost:4444/ui` 可以看到 Grid 狀態與即時 Session 列表；若 Log 顯示 Container 已啟動但 UI 沒反應，記得確認 Docker 是否正常跑在背景。  
- 在 VS Code 執行 Selenium 腳本的同時，觀察 UI 中的 Session，可以驗證腳本是否真的連到遠端 Driver。

## 無頭 Chrome 設定重點
- 雲端 Container 沒有實體螢幕，因此 Headless Chrome 需要預設視窗大小（例如 1280x720），避免被誤判成 mobile viewport。  
- 強制 `--disable-gpu` 以免在沒有 GPU 的環境崩潰，並加入 `--no-sandbox` 讓 ChromeDriver 可以在 Container 內執行。  
- 關閉自動安裝的 extension，確保環境潔淨，必要時在進入網頁前先呼叫 `driver.delete_all_cookies()`。  
- Container 內建的 Chrome Driver 版本固定，若要支援多個 Session，需控管記憶體並針對同一隻 Driver 限制並行工作數。

## 在 Cloud Run Service 佈署 Selenium Grid
- Cloud Run 部署時直接使用 Docker Hub 官方的 `selenium/standalone-chrome` 映像，埠號設定為 4444，記憶體調高到 2GB 以避免同時開多個 Session 時 OOM。  
- 透過「允許未經驗證的呼叫」公開網路端點，並把 Service URL 貼給全班共用。  
- 環境變數需打開允許調整 Session 上限（例如啟用 override flag）、設定最大併發數量、以及調整 JVM heap（`JAVA_OPTS`）來容納多個瀏覽器。  
- Cloud Run 日誌可看到每個請求的啟動/釋放紀錄，搭配 Selenium UI 可以排查腳本失敗點。

## Docker Compose：Flask Demo + Ngrok
- Compose 檔中第一個服務是 `flask-web-server`，用自家 Dockerfile Build，並 `restart: always`、`ports: ["5000:5000"]`、`volumes: .:/app` 方便本機熱重載。  
- 第二個服務使用官方的 `ngrok/ngrok` 映像，`depends_on` Flask，當 Web Server 成功啟動後才 Forward HTTP；同樣設定 `restart: always`，並使用 `links`/共用網路讓 ngrok 能夠內連 `flask-web-server:5000`。  
- 需先到 ngrok 申請帳號取得 auth token，並在 Compose 透過 `NGROK_AUTHTOKEN` 環境變數注入。若想知道 ngrok 給的公開網址，可呼叫它的內建 API（`http://localhost:4040/api/tunnels`）取得 JSON。  
- Compose 幫忙一次啟/停兩個 Container，不需要分別輸入 `docker run`，也可用 `depends_on` 控制順序。

## Docker Compose：Airflow + Postgres 範本
- Airflow 官方預設使用 SQLite，不適合多人與高流量；課堂示範用 Compose 建立 `postgres` + `airflow-webserver` + `airflow-scheduler` 三個服務，並用專屬 volume 保存 `/opt/airflow/{dags,logs}`。  
- `airflow-webserver` 與 `airflow-scheduler` 的 `depends_on` 會檢查 Postgres Health（或至少等待數秒）再啟動，避免發生「資料庫尚未建表」的錯誤。  
- `env_file`/`environment` 事先寫入帳號密碼、資料庫連線字串、預設 Admin 使用者等值，這樣 `docker compose up` 之後即可直接登入 Web UI。  
- 若服務啟動時間過長，可以搭配 `healthcheck` 與 `restart` 策略，確保 Scheduler 掛掉會自動重啟。

## Docker Compose：Kafka、生產者與消費者
- 進一步的 Compose 範例包含 Kafka、Zookeeper、資料庫、Producer/Consumer App 以及專門掛載資料的 volume container；Kafka 必須最先啟動，Producer/Consumer 設 `depends_on` Kafka 的健康狀態。  
- 為了保留訊息與交易紀錄，講師習慣另外開 volume container 而不是直接掛本機資料夾，必要時才把資料拉回本機分析。  
- Compose network 會把所有服務放在同一個虛擬網段，彼此可以直接用服務名稱互相連線，無須再手動 `docker network create`。  
- 若需要關閉整套服務，直接 `docker compose down` 即可，Docker 也會幫忙拆掉自動建立的網路。

## BigQuery Remote Function 概念
- Remote Function 可以在 SQL 中自訂函數，把欄位值丟到 Cloud Run Function 做進階運算，再把結果（例如機器學習標籤）帶回 SQL。  
- Cloud Run Function 如果掛了，Remote Function 也無法使用；課堂僅能以過去案例說明：將使用者輸入的地址送到 Cloud Function，後者呼叫 Google Maps Geocoding API，回傳標準化地址與經緯度，BigQuery 查詢即可直接取得乾淨資料。  
- 實務上可把敏感 API Key 關在 Cloud Function，再由 Remote Function 轉呼叫，避免在 SQL 裡洩漏憑證。

## 其他工具與提醒
- 面對陌生專案時，先確定檔案路徑、埠號、環境變數是否拼對；若要重構，先用 Docker Compose 把原始服務包成一鍵啟動。  
- `uv` 是近期推出、以 Rust 實作的 Python 套件與版本管理工具，指令與 Poetry 幾乎相同，安裝後會自動偵測系統上所有 Python（含 pyenv/homebrew），Lock 檔為 `uv.lock`，速度遠快於以 Python 撰寫的工具。  
- 若已經使用 Poetry，也可以逐步將專案遷移到 `uv`，只需把相關指令中的 `poetry` 改成 `uv` 即可，其他設定（`pyproject.toml`）仍能沿用。
