FROM --platform=$BUILDPLATFORM python:3.11.9-alpine3.20 AS builder
LABEL name="subconv"

# 设置工作目录
WORKDIR /app

# 复制当前目录下的内容到工作目录
COPY . .

# 安装Alpine软件包
RUN apk add --update-cache ca-certificates tzdata patchelf clang ccache

# 安装Python依赖，并安装nuitka
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt nuitka

# 使用Nuitka编译Python为C语言程序
RUN --mount=type=cache,target=/root/.cache/Nuitka \
    python3 -m nuitka --clang --onefile --standalone api.py && \
    chmod +x api.bin

# 使用Alpine镜像
FROM alpine

# 设置工作目录
WORKDIR /app

# 复制必要的内容
COPY --from=builder /app/api.bin /app/api.bin
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY static /app/static
COPY config.yaml /app/config.yaml

# 开放端口访问
EXPOSE 8080

# 启动程序
ENTRYPOINT ["/app/api.bin"]
