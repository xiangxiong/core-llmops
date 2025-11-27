# 项目规则摘要

## 1. 技术栈
- Web框架: Flask 3.0.2
- 依赖注入: injector 0.21.0
- 环境变量: python-dotenv
- AI集成: openai
- 表单验证: flask-wtf
- 数据库: psycopg2 + SQLAlchemy
- 迁移工具: Flask-Migrate

## 2. 目录结构
```
llmops-api/
├── app/               # 应用入口层
├── config/            # 配置文件
├── internal/          # 内部核心模块
├── pkg/               # 公共包
├── test/              # 测试目录
├── storage/           # 存储目录
└── tmp/               # 临时文件
```

## 3. 命名规则
- **文件**: 小写+下划线 (module_name.py)
- **类**: 驼峰命名 (AppHandler, AppService)
- **函数**: 小写+下划线 (create_app, get_app)
- **变量**: 小写+下划线 (user_id, app_name)
- **数据库表**: 小写+下划线 (app, user)

## 4. 编码规范
- 文件头部必须包含标准注释
- 导入顺序: 标准库 → 第三方库 → 内部模块
- 类定义使用 @dataclass 和 @inject 装饰器
- 函数必须有文档字符串和类型注解
- 数据库模型继承自 db.Model
- 每行代码不超过100字符
- 缩进使用4个空格
- 遵循PEP 8规范

## 5. 数据库规范
- 使用UUID作为主键
- 明确表名和约束
- 使用上下文管理器管理事务
- 字段类型和约束明确

## 6. 错误处理
- 使用自定义异常类 FailException
- 统一响应格式
- 表单验证失败返回结构化错误信息

## 7. 配置管理
- 敏感配置通过环境变量管理
- 使用配置类统一管理
- 禁止硬编码敏感信息

## 8. 依赖注入
- 使用 injector 框架
- 模块定义在 module.py 中
- 服务类通过 @inject 注入依赖

## 9. 测试规范
- 测试文件放在 test/ 目录
- 遵循 pytest 框架
- 测试覆盖率不低于80%

## 10. 版本控制
- 使用 .gitignore 忽略敏感文件
- 虚拟环境 .venv 必须被忽略
- 临时文件目录 tmp/ 必须被忽略

## 11. 部署规范
- 生产环境禁止 debug=True
- 数据库连接通过环境变量配置
- 敏感信息不得硬编码

## 12. 文档规范
- 关键类和函数必须有文档字符串
- 复杂逻辑必须有注释
- API接口必须有详细说明

---

详细规范请参考: [PROJECT_STYLE_GUIDE.md](PROJECT_STYLE_GUIDE.md)