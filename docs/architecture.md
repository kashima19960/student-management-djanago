# 架构设计文档 — 学生管理系统

## 1. 系统概述

学生管理系统是一个基于 Django 的 Web 应用，用于管理学生、教师、课程、成绩、考勤等教务数据。系统采用经典的 MVC（MTV）架构，前端使用 Django 模板 + Bootstrap 5，后端提供 REST API，支持多角色权限控制。

## 2. 技术栈

| 层级 | 技术 |
|------|------|
| 语言 | Python 3.8+ |
| Web 框架 | Django 4.2 LTS |
| REST API | Django REST Framework 3.14 |
| 前端 | Bootstrap 5 + Chart.js |
| 数据库 | SQLite (开发) / PostgreSQL (生产) |
| 缓存 | LocMemCache (开发) / Redis (生产) |
| 异步任务 | Celery + Redis |
| 测试 | pytest-django + factory_boy |
| 部署 | Docker + Gunicorn + WhiteNoise |

## 3. 整体架构

```
┌─────────────────────────────────────────────────┐
│                   客户端浏览器                    │
│         Bootstrap 5 + Chart.js + AJAX           │
└────────────┬───────────────────┬────────────────┘
             │ HTTP              │ AJAX
             ▼                   ▼
┌─────────────────────────────────────────────────┐
│               Django 应用层                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ 模板视图  │  │ REST API │  │ Admin 后台   │  │
│  │ (FBV)    │  │ (DRF)    │  │              │  │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
│       │              │               │          │
│  ┌────▼──────────────▼───────────────▼───────┐  │
│  │            权限层 (RBAC)                   │  │
│  │    admin / teacher / student_viewer       │  │
│  └────────────────┬──────────────────────────┘  │
│                   │                              │
│  ┌────────────────▼──────────────────────────┐  │
│  │            数据模型层 (ORM)                │  │
│  │  Student | Teacher | Course | Enrollment  │  │
│  │  Department | ClassInfo | Attendance      │  │
│  │  AuditLog                                │  │
│  └────────────────┬──────────────────────────┘  │
└───────────────────┼─────────────────────────────┘
                    │
         ┌──────────▼──────────┐
         │    数据库 / 缓存     │
         │ SQLite / PostgreSQL  │
         │ Redis (可选)         │
         └─────────────────────┘
```

## 4. 模块划分

```
students/
├── models.py           # 8 个数据模型
├── views.py            # 学生 CRUD + 认证视图
├── views_department.py # 院系管理
├── views_class.py      # 班级管理
├── views_teacher.py    # 教师管理
├── views_course.py     # 课程管理
├── views_grade.py      # 成绩管理
├── views_attendance.py # 考勤管理
├── views_dashboard.py  # 数据统计仪表盘
├── views_import_export.py # 数据导入导出
├── views_report.py     # PDF 报表
├── forms.py            # 所有表单
├── urls.py             # 路由配置
├── admin.py            # Admin 注册
├── decorators.py       # 权限装饰器
├── mixins.py           # CBV 权限混入
├── middleware.py        # 审计日志中间件
├── utils.py            # 工具函数
├── tasks.py            # Celery 异步任务
├── templatetags/
│   └── auth_tags.py    # 权限模板标签
├── api/
│   ├── serializers.py  # DRF 序列化器
│   ├── viewsets.py     # DRF ViewSet
│   ├── permissions.py  # API 权限
│   └── urls.py         # API 路由
└── tests/
    ├── factories.py    # 测试工厂
    ├── test_models.py  # 模型测试
    ├── test_views.py   # 视图测试
    ├── test_forms.py   # 表单测试
    ├── test_api.py     # API 测试
    └── test_permissions.py # 权限测试
```

## 5. 数据模型关系 (ER)

```
Department ─┬─< ClassInfo ─< Student >─< Enrollment >─ Course
            │                                │             │
            ├─< Teacher >────────────────────┘             │
            │                                              │
            └─< Course ─< Attendance >─ Student            │
                                                             │
AuditLog (独立审计表)                                         │
```

### 核心模型字段

- **Department**: code, name, description
- **ClassInfo**: name, department(FK), grade_year, advisor
- **Teacher**: teacher_id, name, department(FK), phone, email, user(O2O)
- **Student**: student_id, name, age, major, class_info(FK), enrollment_date, graduation_date, avatar
- **Course**: course_id, name, credit, teacher(FK), department(FK), max_students
- **Enrollment**: student(FK), course(FK), semester, score, grade_point(auto), status
- **Attendance**: student(FK), course(FK), date, status, remark
- **AuditLog**: user(FK), action, model_name, object_id, changes, ip_address, timestamp

## 6. 权限设计

### 角色矩阵

| 功能 | admin | teacher | student_viewer |
|------|-------|---------|----------------|
| 查看 Dashboard | ✅ | ✅ | ❌ |
| 学生列表 | ✅ | ✅ | ✅ |
| 新增/编辑/删除学生 | ✅ | ❌ | ❌ |
| 院系/班级/教师管理 | ✅ | ❌ | ❌ |
| 课程管理 | ✅ | ❌ | ❌ |
| 成绩录入 | ✅ | ✅(自己的课程) | ❌ |
| 考勤录入 | ✅ | ✅(自己的课程) | ❌ |
| 数据导入导出 | ✅ | ✅ | ❌ |
| 查看统计报表 | ✅ | ✅ | ❌ |
| PDF 成绩单 | ✅ | ✅ | ✅(自己的) |

### 实现机制

1. **Django Groups**: admin, teacher, student_viewer
2. **自定义装饰器**: `@role_required("admin")` 用于 FBV
3. **自定义混入**: `RoleRequiredMixin` 用于 CBV
4. **模板标签**: `{% has_role "admin" as is_admin %}` 控制菜单显示

## 7. API 设计

### RESTful 端点

| 资源 | GET (列表) | POST (创建) | GET (详情) | PUT (更新) | DELETE |
|------|-----------|-------------|-----------|-----------|--------|
| `/api/departments/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/api/classes/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/api/teachers/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/api/courses/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/api/students/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/api/enrollments/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/api/attendances/` | ✅ | ✅ | ✅ | ✅ | ✅ |

### 自定义端点

- `GET /api/students/{id}/enrollments/` — 学生选课记录
- `GET /api/students/{id}/attendances/` — 学生考勤记录
- `GET /api/courses/{id}/enrollments/` — 课程选课学生
- `GET /api/courses/{id}/statistics/` — 课程成绩统计
- `GET /api/teachers/{id}/courses/` — 教师授课列表

### 认证方式

- TokenAuthentication: `Authorization: Token <token>`
- SessionAuthentication: Django session (浏览器访问)

### 文档

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`

## 8. 部署架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Nginx     │────▶│  Gunicorn   │────▶│  Django App  │
│ (反向代理)   │     │ (WSGI)      │     │  (Docker)    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────┐
                    │                          │              │
              ┌─────▼─────┐           ┌───────▼───────┐     │
              │ PostgreSQL │           │    Redis      │     │
              │ (数据库)    │           │ (缓存+Broker) │     │
              └───────────┘           └───────────────┘     │
                                                           │
                                                    ┌──────▼──────┐
                                                    │   Celery    │
                                                    │ (异步任务)   │
                                                    └─────────────┘
```

### Docker 部署

```bash
# 构建
docker build -t student-management .

# 运行
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-secret-key \
  -e DJANGO_ALLOWED_HOSTS=localhost \
  student-management
```

## 9. 安全设计

1. **SECRET_KEY**: 环境变量注入，不硬编码
2. **CSRF**: Django 内置 CSRF 中间件
3. **XSS**: Django 模板自动转义
4. **SQL 注入**: Django ORM 参数化查询
5. **RBAC**: 角色权限控制
6. **审计日志**: 记录所有 CRUD 操作
7. **HTTPS**: 生产环境强制 SSL
8. **密码**: Django 内置密码哈希 (PBKDF2)

## 10. 性能设计

1. **分页**: 所有列表页统一 15 条/页
2. **select_related**: 减少 N+1 查询
3. **缓存**: Dashboard 统计数据缓存 5 分钟
4. **异步**: 批量导入/报表生成使用 Celery
5. **静态文件**: WhiteNoise 压缩+缓存
