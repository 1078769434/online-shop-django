# 使用Python 3官方镜像作为基础镜像
FROM python:3

# 设置环境变量
# Python不会尝试编写.pyc文件
ENV PYTHONDONTWRITEBYTECODE 1
# Python输出是直接送往终端的，不进行缓存
ENV PYTHONUNBUFFERED 1

# 在容器内创建一个目录来存放应用代码，并将其设置为工作目录
WORKDIR /app

# 将当前目录下的内容复制到容器内的 /app 目录下面
COPY . /app

# 安装 pip 包管理器的包依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 运行数据库迁移
RUN python manage.py migrate

# 暴露端口 8000 以供外部连接访问应用
EXPOSE 8000

# 启动 Django 应用服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]