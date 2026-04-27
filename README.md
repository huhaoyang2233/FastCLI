# FastCLI

🚀 **FastCLI** - 基于 OpenAPI Specification 自动生成 CLI，让你的 FastAPI 服务自动拥有 CLI 接口，直接在终端调用 API。生成的 Markdown 文档可直接扔给大模型，一键生成 AI Skill，让 AI 助手帮你调用 API！

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)](https://fastapi.tiangolo.com/)
[![Typer](https://img.shields.io/badge/Typer-0.9%2B-orange)](https://typer.tiangolo.com/)

## ✨ 特性

- 🎯 **零配置**: 一行命令即可从 FastAPI 应用生成完整 CLI
- 🎨 **美观输出**: 使用 Rich 库渲染漂亮的表格和彩色输出
- 📦 **一键安装**: 自动生成 setup.py，支持 pip 安装
- 📝 **自动文档**: 生成 Markdown 格式的 CLI 使用文档
- 🔧 **高度可定制**: 通过 JSON 配置文件自定义命名规则、输出格式等
- 🏷️ **标签分组**: 按照 FastAPI 的 tags 自动分组命令
- 🧠 **AI Skill 就绪**: 生成的 Markdown 文档可直接扔给大模型，快速生成 AI Skill

## 🚀 快速开始

### 1. 安装

```bash
git clone https://github.com/huhaoyang2233/FastCLI.git
cd FastCLI
pip install -e .
```

### 2. 配置

编辑 `cli_generator/config.json`：

```json
{
  "name": "my-api-cli",
  "version": "1.0.0",
  "description": "My API CLI",
  "fastapi": {
    "module": "main:app",
    "base_url": "http://localhost:8000"
  },
  "cli": {
    "entry_point": "mytool",
    "output_file": "cli.py"
  }
}
```

### 3. 生成 CLI

```bash
python cli_generator/generate.py
```

### 4. 使用 CLI

```bash
# 安装生成的 CLI
pip install -e .

# 查看帮助
mytool --help

# 调用 API
mytool users list_users
mytool users get_users_by_id 1
mytool users create_users --data '{"name": "Alice", "email": "alice@example.com"}'
```

## 📁 项目结构

```
FastCLI/
├── cli_generator/          # CLI 生成器核心代码
│   ├── generator.py        # 生成器主逻辑
│   ├── generate.py         # 启动脚本
│   └── config.json         # 配置文件
├── cli.py                  # 生成的 CLI 文件
├── setup.py                # 生成的安装配置
├── main.py                 # 示例 FastAPI 应用
└── README.md               # 本文档
```

## 🛠️ 高级配置

### 命名规则配置

```json
{
  "naming": {
    "list_prefix": "list",      // GET /users -> list_users
    "get_prefix": "get",        // GET /users/{id} -> get_users_by_id
    "create_prefix": "create",  // POST /users -> create_users
    "update_prefix": "update",  // PUT /users/{id} -> update_users_by_id
    "delete_prefix": "delete",  // DELETE /users/{id} -> delete_users_by_id
    "path_param_suffix": "by_id"
  }
}
```

### 输出配置

```json
{
  "output": {
    "generate_setup_py": true,   // 生成 setup.py
    "generate_markdown": true,   // 生成 Markdown 文档
    "output_dir": "."            // 输出目录
  }
}
```

## 📖 示例输出

### 列表查询

```bash
$ mytool users list_users
┏━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━┓
┃ id ┃ name  ┃ email             ┃ age ┃
┡━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━┩
│ 1  │ Alice │ alice@example.com │ 25  │
│ 2  │ Bob   │ bob@example.com   │ 30  │
└────┴───────┴───────────────────┴─────┘
```

### 单条查询

```bash
$ mytool users get_users_by_id 1
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ 字段  ┃ 值                ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ id    │ 1                 │
│ name  │ Alice             │
│ email │ alice@example.com │
│ age   │ 25                │
└───────┴───────────────────┘
```

## 🔧 工作原理

1. **解析 FastAPI 应用**: 通过 `app.openapi()` 获取 OpenAPI 规范
2. **提取端点信息**: 解析路径、方法、参数、请求体、响应模型
3. **生成 Typer 代码**: 根据端点信息生成对应的 CLI 命令
4. **渲染输出**: 使用 Rich 库美化 API 响应的表格展示

## 🧠 AI Skill 扩展

FastCLI 生成的 Markdown 文档（`my-api-cli-cli.md`）可以直接扔给大模型，快速生成 AI Skill，让 AI 助手帮你调用 API！

### 使用场景

将生成的 CLI 文档提供给 AI 助手（如 Claude、GPT 等），AI 可以：
- 🤖 **自动理解 API 结构**: 无需额外说明，AI 直接读取文档了解所有端点
- 💬 **自然语言调用**: 用户用自然语言描述需求，AI 自动转换为 CLI 命令
- 📝 **生成代码**: 基于 API 文档自动生成调用代码
- 🔍 **智能补全**: 提示必填参数、参数类型和示例值

### 示例

假设你将 `my-api-cli-cli.md` 提供给 AI 助手：

**用户**: 帮我创建一个新用户，名字叫张三，邮箱是 zhangsan@example.com

**AI 助手**（基于文档理解）:
```bash
mytool users create_users --data '{"name": "张三", "email": "zhangsan@example.com"}'
```

**用户**: 查看所有商品

**AI 助手**:
```bash
mytool products list_products
```

### 在 Claude 中创建 Skill

1. 打开 Claude 的 Skill 创建界面
2. 将 `my-api-cli-cli.md` 内容粘贴到 Skill 描述中
3. 配置 Skill 名称和触发词
4. 保存后即可在对话中使用

### 提示词模板

```
你是一个 API CLI 助手。以下是可用的 CLI 命令文档：

{{粘贴 my-api-cli-cli.md 内容}}

请根据用户的需求，生成对应的 CLI 命令。如果用户没有提供必需参数，请询问用户。
```

## ⚠️ FastAPI 编写要求

为了确保 FastCLI 能够正确识别和生成 CLI，你的 FastAPI 代码需要满足以下要求：

### 1. 使用标准 HTTP 方法

支持的方法：`GET`, `POST`, `PUT`, `DELETE`, `PATCH`

```python
@app.get("/users")      # ✓ 支持
@app.post("/users")     # ✓ 支持
@app.put("/users/{id}")  # ✓ 支持
@app.delete("/users/{id}")  # ✓ 支持
```

### 2. 添加路由标签 (tags)

使用 `tags` 参数对路由进行分组，CLI 会按标签生成命令组：

```python
@app.get("/users", tags=["users"])      # ✓ 生成 mytool users list_users
@app.get("/products", tags=["products"])  # ✓ 生成 mytool products list_products
```

### 3. 添加文档字符串和 summary

添加 `summary` 和 `docstring`，会显示在 CLI 帮助中：

```python
@app.get("/users", tags=["users"], summary="获取用户列表")
async def list_users():
    """获取所有用户的列表，支持分页"""  # ← 显示在 CLI help 中
    ...
```

### 4. 使用 Pydantic 模型定义请求/响应

使用 Pydantic 模型可以生成更好的 CLI 文档：

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

@app.post("/users", response_model=User, tags=["users"])
async def create_user(user: UserCreate):  # ✓ 会识别请求体
    ...
```

### 5. 使用 Path/Query 参数声明

显式声明参数类型和验证规则：

```python
from fastapi import Path, Query

@app.get("/users/{user_id}", tags=["users"])
async def get_user(
    user_id: int = Path(..., description="用户ID"),  # ✓ 识别为路径参数
    skip: int = Query(0, description="跳过的记录数")  # ✓ 识别为查询参数
):
    ...
```

### 6. 返回 JSON 可序列化的数据

确保响应可以序列化为 JSON：

```python
# ✓ 正确 - 返回 Pydantic 模型
return user

# ✓ 正确 - 返回字典
return {"id": 1, "name": "Alice"}

# ✗ 避免 - 返回 ORM 模型（需要配置 ORM 模式）
return db_user  # 如果没有配置 from_orm 可能会失败
```

### 完整示例

```python
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Path, Query

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

# ✓ 最佳实践示例
@app.get("/users", response_model=List[User], tags=["users"], summary="获取用户列表")
async def list_users(
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(10, description="返回的最大记录数")
):
    """获取所有用户的列表，支持分页"""
    return users_db.values()

@app.get("/users/{user_id}", response_model=User, tags=["users"], summary="获取单个用户")
async def get_user(
    user_id: int = Path(..., description="用户ID")
):
    """根据用户ID获取单个用户信息"""
    return users_db[user_id]

@app.post("/users", response_model=User, tags=["users"], summary="创建用户")
async def create_user(user: UserCreate):
    """创建一个新用户"""
    new_user = User(id=len(users_db) + 1, **user.dict())
    users_db[new_user.id] = new_user
    return new_user
```

遵循以上规范，FastCLI 就能完美识别你的 API 并生成高质量的 CLI 工具！

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

[Apache License 2.0](LICENSE)

---

⭐ 如果这个项目对你有帮助，欢迎 Star 支持！
