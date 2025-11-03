Hello,uuboy
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
