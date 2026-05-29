# API 参考文档 — 学生管理系统

## 认证方式

### Token 认证

```
Authorization: Token <your-token>
```

### 获取 Token

```bash
# 通过 Django Admin 或 shell 创建 Token
python manage.py shell -c "
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import user
user = User.objects.get(username='admin')
token, _ = Token.objects.get_or_create(user=user)
print(token.key)
"
```

## 端点列表

### 院系 `/api/departments/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/departments/` | 院系列表（分页） |
| POST | `/api/departments/` | 创建院系 |
| GET | `/api/departments/{id}/` | 院系详情 |
| PUT | `/api/departments/{id}/` | 更新院系 |
| DELETE | `/api/departments/{id}/` | 删除院系 |

**请求示例 (POST)**:
```json
{
    "code": "CS",
    "name": "计算机科学与技术学院",
    "description": "涵盖软件工程、人工智能等方向"
}
```

### 班级 `/api/classes/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/classes/` | 班级列表 |
| POST | `/api/classes/` | 创建班级 |
| GET | `/api/classes/{id}/` | 班级详情 |
| PUT | `/api/classes/{id}/` | 更新班级 |
| DELETE | `/api/classes/{id}/` | 删除班级 |

**筛选参数**: `department`, `grade_year`

### 教师 `/api/teachers/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/teachers/` | 教师列表 |
| POST | `/api/teachers/` | 创建教师 |
| GET | `/api/teachers/{id}/` | 教师详情 |
| PUT | `/api/teachers/{id}/` | 更新教师 |
| DELETE | `/api/teachers/{id}/` | 删除教师 |
| GET | `/api/teachers/{id}/courses/` | 教师授课列表 |

**筛选参数**: `department`
**搜索参数**: `search` (teacher_id, name)

### 课程 `/api/courses/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/courses/` | 课程列表 |
| POST | `/api/courses/` | 创建课程 |
| GET | `/api/courses/{id}/` | 课程详情 |
| PUT | `/api/courses/{id}/` | 更新课程 |
| DELETE | `/api/courses/{id}/` | 删除课程 |
| GET | `/api/courses/{id}/enrollments/` | 选课学生列表 |
| GET | `/api/courses/{id}/statistics/` | 成绩统计 |

**筛选参数**: `department`, `teacher`
**搜索参数**: `search` (course_id, name)

### 学生 `/api/students/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/students/` | 学生列表 |
| POST | `/api/students/` | 创建学生 |
| GET | `/api/students/{id}/` | 学生详情 |
| PUT | `/api/students/{id}/` | 更新学生 |
| DELETE | `/api/students/{id}/` | 删除学生 |
| GET | `/api/students/{id}/enrollments/` | 学生选课记录 |
| GET | `/api/students/{id}/attendances/` | 学生考勤记录 |

**筛选参数**: `major`, `class_info`
**搜索参数**: `search` (student_id, name, major)

### 选课/成绩 `/api/enrollments/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/enrollments/` | 选课列表 |
| POST | `/api/enrollments/` | 创建选课 |
| GET | `/api/enrollments/{id}/` | 详情 |
| PUT | `/api/enrollments/{id}/` | 更新（录入成绩） |
| DELETE | `/api/enrollments/{id}/` | 删除 |

**筛选参数**: `student`, `course`, `semester`, `status`
**请求示例 (POST - 录入成绩)**:
```json
{
    "student": 1,
    "course": 1,
    "semester": "2024-2025-1",
    "score": 85.5,
    "status": "completed"
}
```

### 考勤 `/api/attendances/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/attendances/` | 考勤列表 |
| POST | `/api/attendances/` | 创建考勤 |
| GET | `/api/attendances/{id}/` | 详情 |
| PUT | `/api/attendances/{id}/` | 更新 |
| DELETE | `/api/attendances/{id}/` | 删除 |

**筛选参数**: `student`, `course`, `date`, `status`

### Dashboard API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/dashboard/api/stats/` | 基础统计 |
| GET | `/dashboard/api/major-distribution/` | 专业分布 |
| GET | `/dashboard/api/age-distribution/` | 年龄分布 |
| GET | `/dashboard/api/enrollment-trend/` | 招生趋势 |
| GET | `/dashboard/api/gpa-distribution/` | GPA 分布 |
| GET | `/dashboard/api/attendance-rate/` | 出勤率 |

**响应示例**:
```json
{
    "labels": ["计算机", "数学", "外语"],
    "values": [10, 8, 7]
}
```

## 通用参数

### 分页

```
GET /api/students/?page=2&page_size=10
```

### 搜索

```
GET /api/students/?search=张三
```

### 排序

```
GET /api/students/?ordering=student_id
GET /api/students/?ordering=-enrollment_date
```

## 错误响应

```json
{
    "detail": "Authentication credentials were not provided."
}
```

| HTTP 状态码 | 含义 |
|------------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## Swagger UI

访问 `/api/docs/` 查看交互式 API 文档，可直接在浏览器中测试 API。
