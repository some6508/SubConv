# docker build -t subconv . && docker run -d --network host --name subconv-app subconv
# docker build -t subconv . && docker run -d -p 8080:8080 --name subconv-app subconv
FROM python:3.11.9-slim-bookworm

# 设置时区为亚洲/上海
ENV TZ=Asia/Shanghai
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -fns /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制当前目录下的内容到 /app 目录
COPY . /app

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 开放端口访问
EXPOSE 8080

# 启动脚本
CMD ["python", "api.py"]
