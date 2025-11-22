# TJR103

## Lecture Notes
- [Docker 課堂筆記（2025/09/23 上午）](docs/Tibame%2020250923%20docker%20morning.md)
- [Docker 課堂筆記（2025/09/23 下午）](docs/Tibame%2020250923%20docker%20afternoon.md)
- [Docker 課堂筆記（2025/10/03 上午）](docs/Tibame%2020251003%20docker%20morning.md)
- [Data Pipeline 課堂筆記（2025/10/03 下午）](docs/Tibame%2020251003%20datapipeline%20afternoon.md)
- [Data Pipeline 課堂筆記（2025/10/03 夜間）](docs/Tibame%2020251003%20datapipeline%20night.md)
- [Data Pipeline 課堂筆記（2025/10/08 夜間）](docs/Tibame%2020251008%20datapipeline%20night.md)
- [Data Pipeline 課堂筆記（2025/10/18 上午）](docs/Tibame%2020251018%20datapipeline%20morning.md)
- [Data Pipeline 課堂筆記（2025/10/18 下午）](docs/Tibame%2020251018%20datapipeline%20afternoon.md)
- [Data Pipeline 課堂筆記（2025/10/22 夜間）](docs/Tibame%2020251022%20datapipeline%20night.md)
- [GCP 課堂筆記（2025/11/01 上午）](docs/Tibame%2020251101%20gcp%20morning.md)
- [Data Pipeline 課堂筆記（2025/11/01 下午）](docs/Tibame%2020251101%20datapipeline%20afternoon.md)
- [Data Pipeline 課堂筆記（2025/11/02 上午）](docs/Tibame%2020251102%20datapipeline%20morning.md)
- [GCP 課堂筆記（2025/11/02 下午）](docs/Tibame%2020251102%20gcp%20afternoon.md)
- [GCP 課堂筆記（2025/11/08 上午）](docs/Tibame%2020251108%20gcp%20morning.md)
- [GCP 課堂筆記（2025/11/08 下午）](docs/Tibame%2020251108%20gcp%20afternoon.md)
- [GCP 課堂筆記（2025/11/16 上午）](docs/tibame_20251116_gcp_morning.md)
- [GCP 課堂筆記（2025/11/22 上午）](docs/Tibame_20251122_GCP_morning.md)

## Quick Notes (2025/10/03)

### Morning | Docker | Dev Container
1. Install extension: Dev Container
2. Check if Docker is running
3. The folder .devcontainer need to be right under the project root folder
4. .devcontainer/devcontainer.json is required
5. Use VSCode command to start dev container (CTRL + SHIFT + P, then type `rebuild`)
6. If stocked on opening devcontainer session, restart VSCode
   - Also remove container and image

### Afternoon | Data Pipeline
#### Prepare environment
1. Install Poetry
   - If Windows:
        ```
        (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
        ```
       - Add environment variable
            ```
            [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\\Users\\<Your User Name>\\AppData\\Roaming\\Python\\Scripts", "User")
            ```
   - If Mac:
       1. Install homebrew
            ```
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            ```
       2. Install pipx with brew
            ```
            brew install pipx
            ```
       3. Install poetry with pipx
            ```
            pipx install poetry
            ```
2. Create virtual environment using Poetry
   1. `poetry init`
   2. Press `Enter` for all options
      1. If git not used: Enter `n` on Author part
   3. `poetry add <package>` to create virtual environment, then you must see environment path
      1. Path can be found in `poetry env info` (Find Python executable)
   4. Select Python interpreter on VSCode
      1. Windows: ctrl + shift + P
      2. Mac: command + shift + P

## Quick Notes (2025/10/18)

### REST API | CRUD
1. Create → insert → `POST`
2. Read → select → `GET`
3. Update → update → `UPDATE`
4. Delete → delete → `DELETE`

### Environment | MySQL
```bash
docker run -d --name mysql-local -e MYSQL_ROOT_PASSWORD=pasword -p 3306:3306 mysql:8
```

## Quick Notes (2025/11/01)

### Airflow Server on GCP
1. GCP Console
   1. 建立 Compute Engine（VM）。
2. 本機終端
   1. 以 `ssh -i <your_private_key_path> <user_name>@<VM_public_IP>` 連線主機。
3. VM 內部
   1. 安裝 Docker 並將使用者加入 docker 群組：
      1. `sudo usermod -aG docker tjr103-gcp-user`
      2. 登出後重新登入讓群組生效。
   2. 透過 `git clone` 取得 `airflow-demo` 專案。
   3. 調整專案權限讓容器可存取：
      1. `sudo chmod -R 777 /home/tjr103-gcp-user/airflow-demo`
   4. 在 `/home/tjr103-gcp-user/airflow-demo` 執行 Docker 版 Airflow。
4. 容器內
   1. 確認 `/opt/airflow/dags` 已同步專案 DAGs。

## Quick Notes (2025/11/02)

### Startup Script
```bash
apt-get update -y
apt-get install -y docker.io
useradd -m tjr103-gcp-user
cd /home/tjr103-gcp-user
git clone https://github.com/uuboyscy/airflow-demo.git
git config --global --add safe.directory /home/tjr103-gcp-user/airflow-demo
chmod -R 777 airflow-demo
cd /home/tjr103-gcp-user/airflow-demo
git config core.filemode false
usermod -aG docker tjr103-gcp-user
docker run -it -d \
  --name airflow-server \
  -p 8080:8080 \
  -v /home/tjr103-gcp-user/airflow-demo/dags:/opt/airflow/dags \
  -v /home/tjr103-gcp-user/airflow-demo/logs:/opt/airflow/logs \
  -v /home/tjr103-gcp-user/airflow-demo/utils:/opt/airflow/utils \
  -v /home/tjr103-gcp-user/airflow-demo/tasks:/opt/airflow/tasks \
  -e PYTHONPATH=/opt/airflow \
  apache/airflow:2.11.0-python3.12 airflow standalone
sleep 15
docker exec airflow-server airflow users create \
  --username airflow \
  --firstname airflow \
  --password airflow \
  --lastname airflow \
  --role Admin \
  --email your_email@example.com
```

### gcloud Provisioning
- 標準規格：`--provisioning-model=STANDARD`，中斷風險低、費用較高。
- Spot 規格：`--provisioning-model=SPOT --instance-termination-action=STOP --max-run-duration=28800s`，成本更低但可能被回收。

```bash
gcloud compute instances create airflow-demo-spot-test \
  --project=notional-zephyr-229707 \
  --zone=asia-east1-a \
  --machine-type=e2-standard-2 \
  --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
  --metadata=enable-osconfig=TRUE,\
startup-script='#!/bin/bash
apt-get update -y
apt-get install -y docker.io git
useradd -m tjr103-gcp-user
cd /home/tjr103-gcp-user
git clone https://github.com/uuboyscy/airflow-demo.git
chmod -R 777 airflow-demo
usermod -aG docker tjr103-gcp-user

docker run -it -d \
  --name airflow-server \
  -p 8080:8080 \
  -v /home/tjr103-gcp-user/airflow-demo/dags:/opt/airflow/dags \
  -v /home/tjr103-gcp-user/airflow-demo/logs:/opt/airflow/logs \
  -v /home/tjr103-gcp-user/airflow-demo/utils:/opt/airflow/utils \
  -v /home/tjr103-gcp-user/airflow-demo/tasks:/opt/airflow/tasks \
  -e PYTHONPATH=/opt/airflow \
  apache/airflow:2.11.0-python3.12 airflow standalone

# wait for Airflow to start up
sleep 15

# create default user
docker exec airflow-server airflow users create \
  --username airflow \
  --firstname airflow \
  --lastname airflow \
  --role Admin \
  --email your_email@example.com \
  --password airflow
' \
  --no-restart-on-failure \
  --maintenance-policy=TERMINATE \
  --provisioning-model=SPOT \
  --instance-termination-action=STOP \
  --max-run-duration=28800s \
  --service-account=30300274673-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --tags=http-server,https-server \
  --create-disk=auto-delete=yes,boot=yes,device-name=airflow-demo-2,\
disk-resource-policy=projects/notional-zephyr-229707/regions/asia-east1/resourcePolicies/default-schedule-1,\
image=projects/ubuntu-os-cloud/global/images/ubuntu-2404-noble-amd64-v20251021,\
mode=rw,size=30,type=pd-balanced \
  --no-shielded-secure-boot \
  --shielded-vtpm \
  --shielded-integrity-monitoring \
  --labels=goog-ops-agent-policy=v2-x86-template-1-4-0,goog-ec-src=vm_add-gcloud \
  --reservation-affinity=none
```

## Quick Notes (2025/11/08)

### External Partition Table
1. 在 GCS 以 Hive 風格建立分區資料夾  
   `gs://<bucket>/demo_partition/<column_name>=<yyyy-mm-dd>/*.csv`  
   例如：`gs://tjr103-demo-allen/demo_partition/dt=2024-05-06/sale.csv`
2. 建立 External Table（含 partition columns）：
   ```sql
   CREATE OR REPLACE EXTERNAL TABLE `<your_dataset>.SalePartitionExternal`
    (
    TransactionID STRING,
    ProductID STRING,
    Quantity INT64,
    SaleDate DATE,
    )
    WITH PARTITION COLUMNS
    OPTIONS (
    format = 'CSV',
    uris = ['gs://<your_bucket>/demo_partition/*'],
    hive_partition_uri_prefix = 'gs://<your_bucket>/demo_partition',
    skip_leading_rows = 1,
    max_bad_records = 1
    );
   ```

### Query data in BigQuery using Python via google-cloud-bigquery
1. 安裝套件：`google-cloud-bigquery`、`pandas`、`db-dtypes`
   ```shell
   poetry add google-cloud-bigquery pandas db-dtypes
   ```
2. 建立 service account 並賦 BigQuery Admin、Storage Object Admin。
3. 下載 JSON 金鑰並在程式載入：
   ```python
   from google.oauth2.service_account import Credentials

   GCP_CREDENTIAL_SCOPE = [
       "https://www.googleapis.com/auth/cloud-platform",
       "https://www.googleapis.com/auth/drive",
       "https://www.googleapis.com/auth/bigquery",
   ]

   BIGQUERY_CREDENTIALS_FILE_PATH = "bigquery-user.json"
   CREDENTIALS = Credentials.from_service_account_file(
       BIGQUERY_CREDENTIALS_FILE_PATH,
       scopes=GCP_CREDENTIAL_SCOPE,
   )
   ```
4. 若要查詢 Google Sheet External Table，需將 service account 加入該 Sheet（至少 Editor）。

### GCP credential
- 於 Python 設定環境變數：
  ```python
  import os

  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = BIGQUERY_CREDENTIALS_FILE_PATH
  ```
- shell 直接 export：
  ```shell
  export GOOGLE_APPLICATION_CREDENTIALS=tjr103/gcp/bigquery-user.json
  ```

### Artifact Registry
1. 建立 service account `artifact-registry-user.json`。
2. Docker login：
   - Windows
        ```powershell
        Get-Content ".\artifact-registry-user.json" -Raw | docker login -u _json_key --password-stdin https://asia-east1-docker.pkg.dev
        ```
   - macOS/Linux
        ```shell
        cat artifact-registry-user.json | docker login -u _json_key --password-stdin https://asia-east1-docker.pkg.dev
        ```
3. 建立映像：在專案資料夾放好 `Dockerfile` 與 `app.py`
   ```dockerfile
   FROM --platform=linux/amd64 python:3.11-slim-bullseye

   WORKDIR /workspace

   COPY . /workspace

   ENV TZ=Asia/Taipei
   ENV FLASK_APP=app.py
   ENV FLASK_RUN_HOST=0.0.0.0

   EXPOSE 5000

   RUN apt-get update -y
   RUN apt-get install curl vim wget procps git -y
   RUN apt-get install -y zsh \
       && echo "Y" | sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

   RUN pip install --upgrade pip
   RUN pip install flask

   CMD ["flask", "run"]
   ```
   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route("/")
   def hello():
       return "<h1>Hello!</h1>"

   if __name__ == "__main__":
       app.run()
   ```
4. 建置映像並標記 Artifact Registry 路徑：
   ```shell
   cd docker-demo
   docker build -f flask.Dockerfile -t asia-east1-docker.pkg.dev/<project>/<repo>/gar-demo:latest .
   ```
   M 系列 Mac 需加入 `--platform=linux/amd64`。
5. 推送映像：
   ```shell
   docker push asia-east1-docker.pkg.dev/<project>/<repo>/gar-demo:latest
   ```

### Secret Manager
```shell
gcloud secrets versions access latest --secret=tjr103-secret
```

### IAM permissions
- bigquery-user
  - BigQuery Admin
  - Storage Object Admin
- secret-manager-viewer
  - Secret Manager Secret Accessor
  - Secret Manager Secret Version Manager
  - Secret Manager Viewer
- artifact-registry-user
  - Artifact Registry Administrator

## Quick Notes (2025/11/08)

### BigQuery Remote Function
- Follow the URL to create remote function
https://cloud.google.com/bigquery/docs/remote-functions#console
1. Create Cloud Run Function
2. Create BigQuery connection
3. Create Remote Function on BigQuery
