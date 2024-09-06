# 使用Python 3.9作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制requirements.txt文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 设置默认端口为3335
ENV PORT=3335

# 暴露端口
EXPOSE $PORT

# 运行应用程序
CMD uvicorn app:app --host 0.0.0.0 --port $PORT