# 员工管理系统（Django）

## 项目简介
这是一个基于 Django 开发的员工管理系统，实现了基础的用户登录、用户管理和部门管理功能。

## 功能模块
- 用户登录与退出登录
- 首页导航栏根据登录状态动态显示
- 用户管理：新增、编辑、删除、列表展示
- 部门管理：新增、编辑、删除、列表展示

## 技术栈
- Python
- Django
- Bootstrap
- SQLite

## 项目亮点
- 使用 Django ORM 操作数据库
- 使用 ModelForm 实现表单校验和数据保存
- 使用 session 实现登录状态记录和页面访问拦截
- 使用模板继承实现公共导航栏和页面复用

## 数据表设计
### Department 部门表
- title：部门名称

### Employee 员工表
- name：姓名
- password：密码
- age：年龄
- account：余额
- create_time：入职时间
- gender：性别
- department：所属部门（外键关联 Department）

## 启动方式
在项目根目录执行：

```bash
python manage.py runserver
http://127.0.0.1:8000/index/