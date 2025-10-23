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
