# CLI Generator - FastAPI 转 CLI 生成器

这是 **FastCLI** 项目的核心生成器模块，负责将 FastAPI 应用自动转换为 Typer CLI 工具。

## 📋 目录

- [架构概览](#架构概览)
- [核心组件](#核心组件)
- [工作流程](#工作流程)
- [配置说明](#配置说明)
- [扩展开发](#扩展开发)

## 架构概览

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   FastAPI App   │────▶│  OpenAPI Spec   │────▶│  CLI Generator  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                        ┌─────────────────┬─────────────┼─────────────┐
                        ▼                 ▼             ▼             ▼
                   ┌─────────┐      ┌─────────┐   ┌─────────┐   ┌─────────┐
                   │ cli.py  │      │setup.py │   │ *.md    │   │egg-info │
                   └─────────┘      └─────────┘   └─────────┘   └─────────┘
```

## 核心组件

### 1. `generator.py` - 核心生成器

包含以下主要类：

#### `CLIGeneratorConfig`
配置数据类，定义生成器的所有配置选项：
- 包信息（名称、版本、描述、作者）
- FastAPI 模块路径和基础 URL
- CLI 命令名称和输出文件
- 命名规则前缀（list/get/create/update/delete）
- 输出选项（setup.py、Markdown 文档）

#### `OpenAPIParser`
OpenAPI 规范解析器：
- 解析 FastAPI 的 OpenAPI JSON
- 提取端点路径、HTTP 方法、参数
- 识别请求体和响应模型
- 按标签分组端点

#### `TyperCLIGenerator`
Typer CLI 代码生成器：
- 生成导入语句（typer、requests、rich）
- 生成 Typer 应用和命令组
- 为每个端点生成对应的 CLI 命令函数
- 生成响应处理代码（表格渲染）

#### `SetupPyGenerator`
setup.py 生成器：
- 生成 Python 包安装配置
- 定义 console_scripts 入口点
- 指定依赖包（typer、requests、rich）

#### `MarkdownDocGenerator`
Markdown 文档生成器：
- 生成 CLI 使用文档
- 包含所有命令的详细说明
- 提供使用示例

#### `FastAPIToCLI`
主控制类，协调整个生成流程。

### 2. `generate.py` - 启动脚本

命令行入口，负责：
- 加载 `config.json` 配置文件
- 调用生成器生成所有文件
- 显示生成进度和结果

### 3. `config.json` - 配置文件

用户配置文件，定义生成器的所有参数。

## 工作流程

```python
# 1. 加载配置
config = CLIGeneratorConfig.from_json("config.json")

# 2. 加载 FastAPI 应用
app = load_fastapi_app("main:app")

# 3. 获取 OpenAPI 规范
openapi_spec = app.openapi()

# 4. 解析端点
parser = OpenAPIParser(openapi_spec)
endpoints = parser.parse_endpoints(config)

# 5. 生成 CLI 代码
generator = TyperCLIGenerator(endpoints, config)
cli_code = generator.generate()

# 6. 保存文件
converter.save_files(cli_code, output_dir)
```

## 配置说明

### 完整配置示例

```json
{
  "name": "my-api-cli",
  "version": "1.0.0",
  "description": "My API CLI Tool",
  "author": "Your Name",
  "author_email": "your.email@example.com",
  
  "fastapi": {
    "module": "main:app",
    "base_url": "http://localhost:8000"
  },
  
  "cli": {
    "entry_point": "mytool",
    "output_file": "cli.py",
    "use_rich": true,
    "use_requests": true
  },
  
  "naming": {
    "list_prefix": "list",
    "get_prefix": "get",
    "create_prefix": "create",
    "update_prefix": "update",
    "delete_prefix": "delete",
    "path_param_suffix": "by_id"
  },
  
  "output": {
    "generate_setup_py": true,
    "generate_markdown": true,
    "output_dir": "."
  }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `name` | string | - | 包名称 |
| `version` | string | - | 版本号 |
| `description` | string | - | 包描述 |
| `author` | string | - | 作者名 |
| `author_email` | string | - | 作者邮箱 |
| `fastapi.module` | string | "main:app" | FastAPI 模块路径 |
| `fastapi.base_url` | string | "http://localhost:8000" | API 基础 URL |
| `cli.entry_point` | string | "api-cli" | CLI 命令名称 |
| `cli.output_file` | string | "cli.py" | 输出文件名 |
| `cli.use_rich` | boolean | true | 使用 Rich 美化输出 |
| `cli.use_requests` | boolean | true | 使用 requests 库 |
| `naming.list_prefix` | string | "list" | 列表查询前缀 |
| `naming.get_prefix` | string | "get" | 单条查询前缀 |
| `naming.create_prefix` | string | "create" | 创建前缀 |
| `naming.update_prefix` | string | "update" | 更新前缀 |
| `naming.delete_prefix` | string | "delete" | 删除前缀 |
| `naming.path_param_suffix` | string | "by_id" | 路径参数后缀 |
| `output.generate_setup_py` | boolean | true | 生成 setup.py |
| `output.generate_markdown` | boolean | true | 生成 Markdown 文档 |
| `output.output_dir` | string | "." | 输出目录 |

## 扩展开发

### 自定义生成器

你可以继承 `TyperCLIGenerator` 来定制代码生成逻辑：

```python
from generator import TyperCLIGenerator

class CustomCLIGenerator(TyperCLIGenerator):
    def _generate_imports(self) -> List[str]:
        # 自定义导入语句
        lines = super()._generate_imports()
        lines.append("import my_custom_module")
        return lines
    
    def _generate_response_handling(self) -> List[str]:
        # 自定义响应处理
        return ["print(response.json())"]
```

### 添加新的输出格式

实现新的生成器类：

```python
class JSONDocGenerator:
    """生成 JSON 格式文档"""
    
    def __init__(self, endpoints: List[EndpointInfo], config: CLIGeneratorConfig):
        self.endpoints = endpoints
        self.config = config
    
    def generate(self) -> str:
        import json
        data = {
            "name": self.config.name,
            "version": self.config.version,
            "commands": [
                {
                    "name": ep.name,
                    "method": ep.method,
                    "path": ep.path
                }
                for ep in self.endpoints
            ]
        }
        return json.dumps(data, indent=2)
```

## 技术栈

- **Python 3.8+**: 核心语言
- **Typer**: CLI 框架
- **Rich**: 终端美化
- **Requests**: HTTP 客户端
- **FastAPI**: 源 API 框架
- **Pydantic**: 数据验证

## 相关链接

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Typer 文档](https://typer.tiangolo.com/)
- [Rich 文档](https://rich.readthedocs.io/)

---

📁 **注意**: 这是 FastCLI 项目的子模块，完整文档请参考项目根目录的 README.md
