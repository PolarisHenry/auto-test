FROM python:3.11-slim-bullseye
# Playwright 无头运行 Chromium 需要这些系统库
# 浏览器必须以无头模式运行（--headed 在 Docker 不可用）

# APT 源替换为清华镜像（加速国内构建）
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libnss3 \
        libnspr4 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libdrm2 \
        libdbus-1-3 \
        libxkbcommon0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        libgbm1 \
        libpango-1.0-0 \
        libcairo2 \
        libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先拷贝 requirements.txt 再安装依赖，利用 Docker 层缓存：
#   代码改动不会触发依赖重新安装
COPY requirements.txt .

# Pip 源替换为清华镜像（加速国内构建），超时设为 100 秒
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=100 -r requirements.txt

# Playwright 下载源替换为 npmmirror（加速国内构建）
# chromium --with-deps 会同时安装 Chromium 及其系统依赖
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
RUN playwright install chromium --with-deps

# 最后拷贝代码（代码频繁变更，放最下面避免破坏上方缓存层）
COPY . .
