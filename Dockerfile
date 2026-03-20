FROM python:3.11-slim

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV PYTHONWARNINGS=ignore::UserWarning
ENV TZ=Asia/Taipei

WORKDIR /LineBot_Badminton

# 安裝 PostgreSQL 必要的運行庫 (psycopg2-binary 運作所需)
RUN apt-get update && apt-get install -y \
    libpq5 \
    tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

# 安裝 Pipenv 並根據 Pipfile.lock 安裝依賴
RUN pip install pipenv && \
    pipenv install --system --deploy && \
    pip uninstall -y pipenv && \
    pip cache purge

# 複製程式碼
COPY . .

# 啟動指令
CMD ["sh", "-c", "uvicorn startup:app --host 0.0.0.0 --port ${PORT:-8080}"]