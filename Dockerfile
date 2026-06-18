FROM python:3.11-slim

# 設定環境變數
ENV PYTHONUNBUFFERED=1 \
    PYTHONWARNINGS=ignore::UserWarning \
    TZ=Asia/Taipei \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /LineBot_Badminton

# 調整：加入非同步驅動可能需要的基礎工具
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

# 安裝 Pipenv 並根據 Pipfile.lock 安裝依賴
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --ignore-pipfile && \
    apt-get purge -y --auto-remove gcc && \
    pip uninstall -y pipenv && \
    pip cache purge

# 複製程式碼
COPY . .

# 啟動指令
CMD ["sh", "-c", "uvicorn startup:app --host 0.0.0.0 --port ${PORT:-8080}"]