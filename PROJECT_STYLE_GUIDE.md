# LLM OPS API 项目规范文档

## 1. 项目技术栈

### 1.1 核心框架与库
- **Web框架**: Flask 3.0.2
- **依赖注入**: injector 0.21.0
- **环境变量管理**: python-dotenv
- **AI模型集成**: openai
- **表单验证**: flask-wtf
- **数据库驱动**: psycopg2
- **ORM框架**: SQLAlchemy
- **数据库迁移**: Flask-Migrate

## 2. 目录结构规范

```
llmops-api/
├── app/               # 应用入口层
│   ├── http/          # HTTP服务入口
├── config/            # 配置文件目录
├── internal/          # 内部核心模块
│   ├── core/          # 核心功能
│   ├── exception/     # 异常定义
│   ├── extension/     # 扩展模块
│   ├── handler/       # 请求处理器
│   ├── middleware/    # 中间件
│   ├── model/         # 数据模型
│   ├── router/        # 路由定义
│   ├── schema/        # 请求/响应模式
│   ├── service/       # 业务逻辑层
├── pkg/               # 公共包
│   ├── response/      # 响应工具
│   ├── sqlalchemy/    # SQLAlchemy工具
├── test/              # 测试目录
├── storage/           # 存储目录
├── tmp/               # 临时文件目录
```

## 3. 命名规范

### 3.1 文件命名
- 使用小写字母和下划线组合
- 模块文件：`module_name.py`
- 配置文件：`config_name.py`

### 3.2 类命名
- 使用驼峰命名法（CamelCase）
- 模型类：`App`, `User`
- 处理器类：`AppHandler`
- 服务类：`AppService`

### 3.3 函数命名
- 使用小写字母和下划线组合
- 函数名描述其功能：`create_app`, `get_app`

### 3.4 变量命名
- 使用小写字母和下划线组合
- 局部变量：`user_id`, `app_name`
- 类属性：`id`, `name`, `created_at`

### 3.5 数据库表命名
- 使用小写字母和下划线组合
- 表名：`app`, `user`
- 主键约束名：`pk_table_name_column_name`
- 索引名：`idx_table_name_column_name`

## 4. 编码规范

### 4.1 文件头部注释
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : YYYY/MM/DD HH:MM
@Author  : author_name
@File    : file_name.py
"""
```

### 4.2 导入规范
- 标准库优先导入
- 第三方库次之
- 内部模块最后导入
- 使用绝对导入路径

```python
import os
import uuid
from dataclasses import dataclass

from injector import inject
from openai import OpenAI

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
```

### 4.3 类定义规范
- 使用 `@dataclass` 装饰器定义数据类
- 使用 `@inject` 装饰器实现依赖注入
- 类文档字符串描述类的用途

```python
@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService
```

### 4.4 函数定义规范
- 函数文档字符串描述函数功能
- 参数和返回值类型注解
- 保持函数简洁，单一职责原则

```python
def create_app(self) -> App:
    """调用服务创建新的APP记录"""
    app = self.app_service.create_app()
    return success_message(f"应用已经成功创建，id为{app.id}")
```

### 4.5 数据库模型规范
- 继承自 `db.Model`
- 明确表名和表参数
- 使用类型注解
- 默认值和空值约束明确

```python
class App(db.Model):
    """AI应用基础模型类"""
    __tablename__ = "app"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_app_id"),
        Index("idx_app_account_id", "account_id"),
    )

    id = Column(UUID, default=uuid.uuid4, nullable=False)
    name = Column(String(255), default="", nullable=False)
```

## 5. 错误处理规范

- 使用自定义异常类：`FailException`
- 统一响应格式：`success_json`, `validate_error_json`, `success_message`
- 表单验证失败时返回结构化错误信息

## 6. 数据库操作规范

- 使用上下文管理器进行事务管理：`with self.db.auto_commit()`
- 查询操作使用链式调用
- 使用UUID作为主键
- 时间字段使用`datetime.now`

## 7. 配置管理规范

- 使用环境变量存储敏感配置
- 通过 `dotenv.load_dotenv()` 加载环境变量
- 使用配置类管理应用配置

## 8. 依赖注入规范

- 使用 injector 框架进行依赖注入
- 模块定义在 `module.py` 中
- 服务类通过 `@inject` 装饰器注入依赖

## 9. 代码风格要求

- 每行代码长度不超过100个字符
- 缩进使用4个空格
- 类和函数之间空两行
- 方法之间空一行
- 遵循PEP 8规范

## 10. 文档规范

- 关键类和函数必须有文档字符串
- 复杂逻辑必须有注释
- API接口必须有详细说明

## 11. 版本控制规范

- 使用 `.gitignore` 忽略敏感文件和临时文件
- 虚拟环境目录 `.venv` 必须被忽略
- 临时文件目录 `tmp/` 必须被忽略
- IDE配置文件 `.idea/` 可以选择性忽略

## 12. 测试规范

- 测试文件放在 `test/` 目录下
- 遵循pytest框架规范
- 测试覆盖率不低于80%

## 13. 部署规范

- 生产环境禁止使用 `debug=True`
- 数据库连接信息通过环境变量配置
- 敏感信息不得硬编码在代码中
