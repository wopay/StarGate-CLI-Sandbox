# 1. 改用 DaoCloud 的鏡像加速源 (穩定性極高)
FROM docker.m.daocloud.io/library/node:20-slim

# (備用方案：如果上面那行還是報錯 timeout，請換成這行👇)
# FROM docker.nju.edu.cn/library/node:20-slim

# 2. 注入您的 Clash 代理，確保後續的 apt 和 npm 能順利翻牆
ENV HTTP_PROXY="http://Clash:OCCR2wKy@192.168.2.22:7893"
ENV HTTPS_PROXY="http://Clash:OCCR2wKy@192.168.2.22:7893"
ENV ALL_PROXY="socks5://Clash:OCCR2wKy@192.168.2.22:7893"

# 安裝 Python 與基礎工具 (新增 procps 和 docker.io 補齊雷達武器庫)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    procps \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# 全域安裝 Gemini CLI
#RUN npm install -g @google/gemini-cli

# 🛡️ 架构师防爆版：全域安装 Gemini CLI (注入防断流与镜像装甲)
RUN npm config set registry https://registry.npmmirror.com/ && \
    npm config set strict-ssl false && \
    npm install -g @google/gemini-cli --fetch-retries=5 --fetch-retry-mintimeout=20000 --network-timeout=100000

# 安裝 Python 任務雷達需要的依賴
RUN pip3 install httpx --break-system-packages

WORKDIR /app
CMD ["tail", "-f", "/dev/null"]