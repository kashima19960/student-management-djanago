# 学生管理系统 (Student Management System)

基于 Django 的全功能学生管理系统，支持学生、教师、课程、成绩、考勤的全方位管理。

## 功能特性

- 📋 **学生管理** — CRUD、搜索、分页、Excel 导入导出
- 🏫 **院系/班级管理** — 院系和班级的层级管理
- 👨‍🏫 **教师管理** — 教师信息和授课管理
- 📚 **课程管理** — 课程信息、选课管理
- 📝 **成绩管理** — 批量录入、统计分析、绩点自动计算
- 📅 **考勤管理** — 批量录入、出勤率统计
- 📊 **数据仪表盘** — Chart.js 可视化图表
- 🔐 **RBAC 权限** — 管理员/教师/学生三级角色
- 📄 **PDF 报表** — 生成学生成绩单
- 🔄 **REST API** — DRF 全套 API + Swagger 文档

## 技术栈

- Python 3.8+ / Django 4.2 LTS
- Django REST Framework / Bootstrap 5 / Chart.js
- SQLite (开发) / PostgreSQL (生产)
- Redis + Celery (可选异步任务)
- pytest-django + factory_boy (测试)

## 快速开始

### 本地开发

```bash
# 1. 克隆项目
git clone <repo-url>
cd student-management-django

# 2. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install -r requirements/dev.txt

# 4. 迁移数据库
python manage.py migrate

# 5. 填充演示数据
python manage.py seed_data

# 6. 启动开发服务器
python manage.py runserver
```

访问 http://127.0.0.1:8000/，使用 `admin` / `admin123` 登录。

### Docker 部署

```bash
docker build -t student-management .
docker run -p 8000:8000 -e DJANGO_SECRET_KEY=your-key student-management
```

## 项目结构

```
student-management-django/
├── student_management/     # Django 项目配置
│   ├── settings/           # 分环境配置 (base/dev/prod)
│   ├── celery.py           # Celery 配置
│   └── urls.py             # 主路由
├── students/               # 主应用
│   ├── models.py           # 8 个数据模型
│   ├── views*.py           # 各模块视图
│   ├── forms.py            # 表单
│   ├── api/                # REST API
│   ├── tests/              # 测试用例
│   ├── decorators.py       # 权限装饰器
│   └── templatetags/       # 模板标签
├── templates/              # 24 个模板文件
├── docs/                   # 文档
│   ├── architecture.md     # 架构设计
│   ├── test_plan.md        # 测试方案
│   └── api_reference.md    # API 参考
└── requirements/           # 分层依赖
```

## 角色说明

| 角色 | 用户名/密码 | 权限 |
|------|------------|------|
| 管理员 | admin / admin123 | 全部功能 |
| 教师 | - | 成绩/考勤管理、查看统计 |
| 学生 | - | 查看学生列表 |

## 文档

- [架构设计文档](docs/architecture.md)
- [测试方案文档](docs/test_plan.md)
- [API 参考文档](docs/api_reference.md)
- Swagger UI: http://127.0.0.1:8000/api/docs/

## 运行测试

```bash
pytest students/tests/ -v
pytest students/tests/ --cov=students --cov-report=term-missing
```

## 许可证

MIT License
