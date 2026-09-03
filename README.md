# LineBot_Badminton (羽球助手)

這是一個專為羽球社群設計的自動化管理系統。解決球團管理者在發送通知、統計出席、結算紀錄及整理名單時的繁瑣手動流程。透過 Line
Bot 實現全面自動化，並提供標準化 API 供開發者與管理者進行驗證。

## Engineering Highlights

* **Domain-Driven Design (DDD)**: 嚴格區分業務邏輯（Domain）與基礎設施（Infrastructure），確保架構層次分明，即便未來功能擴充或切換通訊平台也能輕鬆達成。
* **API-First Design**: 核心功能皆透過 FastAPI 設計為 RESTful API，開發者可直接使用 Postman 進行介面測試，確保業務邏輯的正確性。
* **Static Code Analysis**: 使用 Ruff 進行代碼檢查，嚴格遵守 PEP 8 規範與 Type Hinting，維持極高的代碼可讀性與維護性。
* **Lightweight & Reliable**: 針對中小型社群優化，採用非同步模型（async/await）確保在高併發環境下的穩定性與開發效率。

## 啟動Server步驟 - 專案環境設定

### 1. 環境設定

本專案使用 `Pipenv` 套件來統一管理 Python 從外部 PyPI 下載的套件包，因此在開始前要先安裝 `Pipenv`，並了解基本的虛擬環境概念。

```bash
$ brew install pipenv
$ cd LineBot_Badminton
$ mkdir .venv
$ pipenv install
$ pipenv shell
```

### 2. 環境參數設定

本專案使用`.env`檔案管理參數。 請將`.env.example`改為`.env`並填入參數。  
DATABASE_URL 的格式會依據你是連接本地 Docker 或 Fly.io Proxy 而有所不同：

```bash
LINE_CHANNEL_ACCESS_TOKEN=
LINE_CHANNEL_SECRET=
PROFILE_ENDPOINT=
REPLY_ENDPOINT=

OPENTELEMETRY_ENDPOINT=
OPENTELEMETRY_ENABLE=

DATABASE_URL=

BADMINTON_TIME=
BADMINTON_LOCATION=
```

### 3. 運行開發環境

#### 1. 安裝 Docker

在 Docker 官網下載
docker-for-mac([https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/))

#### 2. 建立 Local 環境

只需執行下方指令即可一鍵啟動本地開發環境，包含自動建立資料庫、執行 migration（自動建立 Schema 與 Table），無需手動操作。

```bash
# 建立 local 環境
$ make local-env

# 如果想確認 docker 是否有建立完成
$ docker ps -a
```

關閉測試環境。環境關閉時會將所有資料刪除，包含 Schema 及已經建立的資料，請小心使用。

```bash
# 關閉測試環境
$ make local-env-rm
```

#### 3. 啟動 Local Server

請在 PyCharm 中建立一個 Python 執行物件（Run/Debug Configuration），參數對照表如下：

| Field                 | Value                                      | Description                |
|:----------------------|:-------------------------------------------|:---------------------------|
| Name                  | `debug`                                    | 配置名稱                       |
| Run type              | `module`                                   | 以 Python 模組形式啟動            |
| Module name           | `uvicorn`                                  | ASGI 伺服器                   |
| Parameters            | `startup:app --host 127.0.0.1 --port 8080` | startup:app 指向 FastAPI 進入點 |
| Working directory     | `~/LineBot_Badminton`                      | 指向專案根目錄                    |
| Environment variables | `PYTHONUNBUFFERED=1;ENV={env.value}`       | 透過 ENV 決定環境                |

## 上版步驟

本專案部署於 Fly.io，需要先透過`brew`安裝`Fly CLI`：

```bash
$ brew install flyctl
```

下載完`Fly CLI`後，請先登入 Fly.io 帳號：

```bash
$ fly auth login
```

部署前請先建立資料庫。 此次示範為 Fly.io 的 PostgreSQL 資料庫，可以按照個人的習慣使用不同的資料庫：

```bash
$ fly postgres create
```

Fly.io PostgreSQL 會自動生成一組`DATABASE_URL`，部署前請先將該 URL 設定到環境變數中。  
本地無法直接連線到 Fly.io 的 PostgreSQL，若需要在本地測試資料庫連線，可以使用`fly proxy`指令，將本地的`5432`端口轉發到
Fly.io 的 PostgreSQL 端口。在`Terminal`執行以下指令，即可連接資料庫：

```bash
# 範例：將遠端 5432 映射至本地 5432
# fly proxy 5432:5432 -a template-db
$ fly proxy <Database-Port> -a <Database-Name>
```

Database 建立完成後，將顯示的參數按照以下的提示組成`DATABASE_URL`，並設定到環境變數中：

```bash
postgres://<User-Name>:<Password>@<Service-Name>.flycast:<Database-Port>/<Database-Name>
```

正式環境使用`fly secrets set`指令安全注入敏感資訊（如 Line Secret）。

```bash
$ fly secrets set \
  LINE_CHANNEL_ACCESS_TOKEN="TOKEN" \
  LINE_CHANNEL_SECRET="SECRET" \
  PROFILE_ENDPOINT="ENDPOINT" \
  REPLY_ENDPOINT="ENDPOINT" \
  OPENTELEMETRY_ENDPOINT="OTEL_ENDPOINT" \
  OPENTELEMETRY_ENABLE="true or false" \
  DATABASE_URL="URK" \
  BADMINTON_TIME="TIME" \
  BADMINTON_LOCATION="LOCATION"
```

本專案已經寫有 `fly.toml` 配置檔，部署時只需在專案根目錄下執行以下指令， Fly.io 就會自動部署：

```bash
$ fly deploy  # 部署
$ fly logs  # 查看 VM Logs
```

---

_Last updated: 2026-04-10_

Maintainer: Lucas Lu
