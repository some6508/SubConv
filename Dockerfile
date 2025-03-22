FROM python:3.9.5-slim-buster
LABEL name="subconv"

# 复制当前目录下的内容到 /app 目录
COPY . /app

# 设置时区为亚洲/上海
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN pip install -r requirements.txt

# 开放端口访问
EXPOSE 8080

# 启动脚本
CMD ["python", "api.py"]
