# 学生管理系统（Django）

## 项目背景

这是一个基于 Django 的学生管理系统，包含用户注册、登录、注销以及学生信息的增删改查与搜索功能，适用于教学管理或课程项目演示。

## 本地运行步骤

> Python 版本：3.8.10

1. 创建并激活虚拟环境（目录名必须为 `.venv`）：

```
python -m venv .venv
```

Windows PowerShell：
```
.\.venv\Scripts\Activate.ps1
```

2. 安装依赖：

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. 数据库迁移：

```
python manage.py makemigrations
python manage.py migrate
```

4. 启动服务：

```
python manage.py runserver
```

访问：http://127.0.0.1:8000/

## Docker 运行命令

1. 构建镜像：

```
docker build -t student-management:latest .
```

2. 运行容器（宿主机端口 8302 映射到容器 8000）：

```
docker run --name student-management -p 8302:8000 student-management:latest
```

访问：http://127.0.0.1:8302/
