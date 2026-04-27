#!/usr/bin/env python3
"""
FastAPI 转 Typer CLI 通用生成器

这是一个通用工具，可以将任何 FastAPI 应用的 OpenAPI 规范转换为 Typer CLI。
支持生成 setup.py 打包文件、console_scripts 入口点和 Markdown 文档。
"""

import json
import re
import sys
import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field


@dataclass
class EndpointInfo:
    """端点信息"""
    name: str
    method: str
    path: str
    summary: str
    description: str
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    request_body: Optional[Dict[str, Any]] = None
    response_model: Optional[str] = None
    tag: str = "default"


@dataclass
class CLIGeneratorConfig:
    """CLI 生成器配置"""
    name: str = "api-cli"
    version: str = "1.0.0"
    description: str = "Auto-generated CLI from FastAPI"
    author: str = ""
    author_email: str = ""
    fastapi_module: str = "main:app"
    base_url: str = "http://localhost:8000"
    entry_point: str = "api-cli"
    output_file: str = "cli.py"
    use_rich: bool = True
    use_requests: bool = True
    list_prefix: str = "list"
    get_prefix: str = "get"
    create_prefix: str = "create"
    update_prefix: str = "update"
    delete_prefix: str = "delete"
    path_param_suffix: str = "by_id"
    generate_setup_py: bool = True
    generate_markdown: bool = True
    output_dir: str = "."
    
    @classmethod
    def from_json(cls, json_path: Union[str, Path]) -> "CLIGeneratorConfig":
        """从 JSON 文件加载配置"""
        json_path = Path(json_path)
        if not json_path.exists():
            raise FileNotFoundError(f"找不到配置文件: {json_path}")
        
        data = json.loads(json_path.read_text(encoding='utf-8'))
        
        config = cls()
        config.name = data.get("name", config.name)
        config.version = data.get("version", config.version)
        config.description = data.get("description", config.description)
        config.author = data.get("author", config.author)
        config.author_email = data.get("author_email", config.author_email)
        
        fastapi_config = data.get("fastapi", {})
        config.fastapi_module = fastapi_config.get("module", config.fastapi_module)
        config.base_url = fastapi_config.get("base_url", config.base_url)
        
        cli_config = data.get("cli", {})
        config.entry_point = cli_config.get("entry_point", config.entry_point)
        config.output_file = cli_config.get("output_file", config.output_file)
        config.use_rich = cli_config.get("use_rich", config.use_rich)
        config.use_requests = cli_config.get("use_requests", config.use_requests)
        
        naming_config = data.get("naming", {})
        config.list_prefix = naming_config.get("list_prefix", config.list_prefix)
        config.get_prefix = naming_config.get("get_prefix", config.get_prefix)
        config.create_prefix = naming_config.get("create_prefix", config.create_prefix)
        config.update_prefix = naming_config.get("update_prefix", config.update_prefix)
        config.delete_prefix = naming_config.get("delete_prefix", config.delete_prefix)
        config.path_param_suffix = naming_config.get("path_param_suffix", config.path_param_suffix)
        
        output_config = data.get("output", {})
        config.generate_setup_py = output_config.get("generate_setup_py", config.generate_setup_py)
        config.generate_markdown = output_config.get("generate_markdown", config.generate_markdown)
        config.output_dir = output_config.get("output_dir", config.output_dir)
        
        return config


class OpenAPIParser:
    """OpenAPI JSON 解析器"""
    
    def __init__(self, openapi_spec: Dict[str, Any]):
        self.spec = openapi_spec
        self.schemas = openapi_spec.get("components", {}).get("schemas", {})
        self.tags = {tag.get("name", "default"): tag for tag in openapi_spec.get("tags", [])}
    
    def parse_endpoints(self, config: CLIGeneratorConfig) -> List[EndpointInfo]:
        """解析所有端点"""
        endpoints = []
        paths = self.spec.get("paths", {})
        
        for path, methods in paths.items():
            for method, details in methods.items():
                if method in ("get", "post", "put", "delete", "patch"):
                    endpoint = self._parse_endpoint(path, method, details, config)
                    endpoints.append(endpoint)
        
        return endpoints
    
    def _parse_endpoint(self, path: str, method: str, details: Dict[str, Any], config: CLIGeneratorConfig) -> EndpointInfo:
        """解析单个端点"""
        name = self._generate_function_name(method, path, config)
        
        tags = details.get("tags", [])
        tag = tags[0] if tags else "default"
        
        parameters = []
        for param in details.get("parameters", []):
            param_info = {
                "name": param["name"],
                "in": param["in"],
                "type": self._get_python_type(param.get("schema", {})),
                "required": param.get("required", False),
                "description": param.get("description", ""),
                "default": param.get("schema", {}).get("default")
            }
            parameters.append(param_info)
        
        request_body = None
        if "requestBody" in details:
            content = details["requestBody"].get("content", {})
            if "application/json" in content:
                schema = content["application/json"].get("schema", {})
                request_body = {
                    "schema": schema,
                    "python_type": self._get_python_type(schema),
                    "required": details["requestBody"].get("required", False)
                }
        
        response_model = None
        responses = details.get("responses", {})
        for code in ["200", "201", "202"]:
            if code in responses:
                success_response = responses[code]
                content = success_response.get("content", {})
                if "application/json" in content:
                    schema = content["application/json"].get("schema", {})
                    response_model = self._get_python_type(schema)
                    break
        
        return EndpointInfo(
            name=name,
            method=method.upper(),
            path=path,
            summary=details.get("summary", ""),
            description=details.get("description", ""),
            parameters=parameters,
            request_body=request_body,
            response_model=response_model,
            tag=tag
        )
    
    def _generate_function_name(self, method: str, path: str, config: CLIGeneratorConfig) -> str:
        """生成函数名"""
        clean_path = re.sub(r'\{[^}]+\}', '', path)
        parts = [p for p in clean_path.split('/') if p]
        
        if not parts:
            return f"{method}_root"
        
        has_path_param = "{" in path
        
        if method == "get":
            action = config.get_prefix if has_path_param else config.list_prefix
        elif method == "post":
            action = config.create_prefix
        elif method == "put":
            action = config.update_prefix
        elif method == "patch":
            action = config.update_prefix
        elif method == "delete":
            action = config.delete_prefix
        else:
            action = method
        
        resource = "_".join(parts)
        
        if has_path_param:
            return f"{action}_{resource}_{config.path_param_suffix}"
        
        return f"{action}_{resource}"
    
    def _get_python_type(self, schema: Dict[str, Any]) -> str:
        """将 JSON Schema 类型转换为 Python 类型"""
        if "$ref" in schema:
            ref = schema["$ref"]
            type_name = ref.split("/")[-1]
            return type_name
        
        schema_type = schema.get("type", "any")
        
        type_map = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict"
        }
        
        if schema_type == "array":
            items = schema.get("items", {})
            item_type = self._get_python_type(items)
            return f"List[{item_type}]"
        
        return type_map.get(schema_type, "Any")


class TyperCLIGenerator:
    """Typer CLI 代码生成器 - 使用 entry_point 作为命令名"""
    
    def __init__(self, endpoints: List[EndpointInfo], config: CLIGeneratorConfig):
        self.endpoints = endpoints
        self.config = config
    
    def generate(self) -> str:
        """生成完整的 CLI 代码"""
        lines = []
        
        lines.extend(self._generate_imports())
        lines.append("")
        lines.extend(self._generate_constants())
        lines.append("")
        lines.extend(self._generate_app())
        lines.append("")
        lines.extend(self._generate_command_groups())
        lines.append("")
        lines.extend(self._generate_main())
        
        return "\n".join(lines)
    
    def _generate_imports(self) -> List[str]:
        """生成导入语句"""
        lines = [
            "#!/usr/bin/env python3",
            '"""',
            f"{self.config.description}",
            "由 FastAPI 服务自动生成",
            '"""',
            "",
            "import json",
            "from typing import Optional, List",
            "import typer",
        ]
        
        if self.config.use_requests:
            lines.append("import requests")
        
        if self.config.use_rich:
            lines.extend([
                "from rich.console import Console",
                "from rich.table import Table",
                "from rich import print as rprint",
            ])
        else:
            lines.append("from pprint import pprint")
        
        lines.append("")
        return lines
    
    def _generate_constants(self) -> List[str]:
        """生成常量定义"""
        return [
            f'BASE_URL = "{self.config.base_url}"',
        ]
    
    def _generate_app(self) -> List[str]:
        """生成 Typer 应用"""
        lines = [
            "# 初始化",
            f"app = typer.Typer(help='{self.config.description}', add_completion=False)",
        ]
        
        if self.config.use_rich:
            lines.append("console = Console()")
        
        lines.append("")
        
        # 按标签分组
        tags = set(ep.tag for ep in self.endpoints)
        for tag in sorted(tags):
            safe_tag = self._make_safe_name(tag)
            lines.append(f"{safe_tag}_app = typer.Typer(help='{tag} 相关命令')")
        
        lines.append("")
        
        for tag in sorted(tags):
            safe_tag = self._make_safe_name(tag)
            lines.append(f"app.add_typer({safe_tag}_app, name='{safe_tag}')")
        
        return lines
    
    def _generate_command_groups(self) -> List[str]:
        """生成命令组"""
        lines = []
        
        tags = set(ep.tag for ep in self.endpoints)
        for tag in sorted(tags):
            tag_endpoints = [ep for ep in self.endpoints if ep.tag == tag]
            safe_tag = self._make_safe_name(tag)
            
            for endpoint in tag_endpoints:
                lines.extend(self._generate_endpoint_command(endpoint, f"{safe_tag}_app"))
                lines.append("")
        
        return lines
    
    def _generate_endpoint_command(self, endpoint: EndpointInfo, app_name: str) -> List[str]:
        """生成单个端点命令"""
        lines = []
        
        func_name = endpoint.name.replace("-", "_")
        
        params = []
        
        # 路径参数
        for param in endpoint.parameters:
            if param["in"] == "path":
                param_type = param["type"]
                params.append(f"{param['name']}: {param_type}")
        
        # 查询参数
        for param in endpoint.parameters:
            if param["in"] == "query":
                param_type = param["type"]
                if not param["required"]:
                    default = param.get("default")
                    if default is not None:
                        if param_type == "str":
                            params.append(f"{param['name']}: Optional[{param_type}] = typer.Option('{default}', help='{param['description']}')")
                        else:
                            params.append(f"{param['name']}: Optional[{param_type}] = typer.Option({default}, help='{param['description']}')")
                    else:
                        params.append(f"{param['name']}: Optional[{param_type}] = typer.Option(None, help='{param['description']}')")
                else:
                    params.append(f"{param['name']}: {param_type} = typer.Option(..., help='{param['description']}')")
        
        # 请求体参数
        if endpoint.request_body:
            params.append(f"data: Optional[str] = typer.Option(None, help='请求体 JSON 字符串')")
        
        params_str = ", ".join(params) if params else ""
        lines.append(f"@{app_name}.command(name='{func_name}', help='''{endpoint.summary}''')")
        lines.append(f"def {func_name}({params_str}):")
        lines.append(f'    """{endpoint.description or endpoint.summary}"""')
        lines.append("    try:")
        
        url = endpoint.path
        lines.append(f'        url = f"{{BASE_URL}}{url}"')
        
        query_params = [p for p in endpoint.parameters if p["in"] == "query"]
        if query_params:
            lines.append("        params = {}")
            for param in query_params:
                param_name = param['name']
                lines.append(f"        if {param_name} is not None:")
                lines.append(f"            params['{param_name}'] = {param_name}")
            lines.append("")
        
        method = endpoint.method.lower()
        
        if endpoint.request_body:
            lines.append("        # 解析请求体")
            lines.append("        json_data = json.loads(data) if data else None")
            if query_params:
                lines.append(f"        response = requests.{method}(url, params=params, json=json_data)")
            else:
                lines.append(f"        response = requests.{method}(url, json=json_data)")
        else:
            if query_params:
                lines.append(f"        response = requests.{method}(url, params=params)")
            else:
                lines.append(f"        response = requests.{method}(url)")
        
        lines.append("")
        lines.extend(self._generate_response_handling())
        
        lines.append("")
        lines.append("    except Exception as e:")
        if self.config.use_rich:
            lines.append("        rprint(f'[red]错误: {e}[/red]')")
        else:
            lines.append("        print(f'错误: {e}')")
        lines.append("        raise typer.Exit(1)")
        
        return lines
    
    def _generate_response_handling(self) -> List[str]:
        """生成响应处理代码"""
        lines = []
        
        lines.append("        if response.status_code in [200, 201, 202]:")
        lines.append("            result = response.json()")
        
        if self.config.use_rich:
            lines.extend([
                "            if isinstance(result, list):",
                "                if result:",
                "                    table = Table(show_header=True, header_style='bold magenta')",
                "                    for key in result[0].keys():",
                "                        table.add_column(str(key))",
                "                    for item in result:",
                "                        table.add_row(*[str(v) for v in item.values()])",
                "                    console.print(table)",
                "                else:",
                "                    rprint('[yellow]暂无数据[/yellow]')",
                "            else:",
                "                table = Table(show_header=True, header_style='bold green')",
                "                table.add_column('字段')",
                "                table.add_column('值')",
                "                for key, value in result.items():",
                "                    table.add_row(str(key), str(value))",
                "                console.print(table)",
            ])
        else:
            lines.extend([
                "            pprint(result)",
            ])
        
        lines.append("        else:")
        if self.config.use_rich:
            lines.append("            rprint(f'[red]请求失败: {response.status_code}[/red]')")
            lines.append("            rprint(response.text)")
        else:
            lines.append("            print(f'请求失败: {response.status_code}')")
            lines.append("            print(response.text)")
        
        return lines
    
    def _generate_main(self) -> List[str]:
        """生成主函数"""
        return [
            "def main():",
            "    app()",
            "",
            "if __name__ == '__main__':",
            "    main()",
        ]
    
    def _make_safe_name(self, name: str) -> str:
        """将名称转换为安全的 Python 标识符"""
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        if safe[0].isdigit():
            safe = '_' + safe
        return safe.lower()


class SetupPyGenerator:
    """setup.py 生成器"""
    
    def __init__(self, config: CLIGeneratorConfig):
        self.config = config
    
    def generate(self) -> str:
        """生成 setup.py 内容"""
        lines = [
            "from setuptools import setup, find_packages",
            "",
            "setup(",
            f'    name="{self.config.name}",',
            f'    version="{self.config.version}",',
            f'    description="{self.config.description}",',
        ]
        
        if self.config.author:
            lines.append(f'    author="{self.config.author}",')
        if self.config.author_email:
            lines.append(f'    author_email="{self.config.author_email}",')
        
        lines.extend([
            "    py_modules=[" + f'"{self.config.output_file.replace(".py", "")}"' + "],",
            "    install_requires=[",
            "        'typer>=0.9.0',",
            "        'requests>=2.31.0',",
        ])
        
        if self.config.use_rich:
            lines.append("        'rich>=13.7.0',")
        
        lines.extend([
            "    ],",
            "    entry_points={",
            "        'console_scripts': [",
            f'            "{self.config.entry_point}={self.config.output_file.replace(".py", "")}:main",',
            "        ],",
            "    },",
            ")",
        ])
        
        return "\n".join(lines)


class MarkdownDocGenerator:
    """Markdown 文档生成器"""
    
    def __init__(self, endpoints: List[EndpointInfo], config: CLIGeneratorConfig):
        self.endpoints = endpoints
        self.config = config
    
    def generate(self) -> str:
        """生成 Markdown 文档"""
        lines = []
        
        # 标题
        lines.append(f"# {self.config.name}")
        lines.append("")
        lines.append(f"{self.config.description}")
        lines.append("")
        lines.append(f"- **版本**: {self.config.version}")
        lines.append(f"- **API 基础 URL**: {self.config.base_url}")
        lines.append(f"- **CLI 命令**: `{self.config.entry_point}`")
        lines.append("")
        
        # 安装说明
        lines.append("## 安装")
        lines.append("")
        lines.append("```bash")
        lines.append("pip install -e .")
        lines.append("```")
        lines.append("")
        
        # 使用说明
        lines.append("## 使用")
        lines.append("")
        lines.append(f"安装后，可以使用 `{self.config.entry_point}` 命令来访问 API。")
        lines.append("")
        
        # 命令列表
        lines.append("## 命令列表")
        lines.append("")
        
        # 按标签分组
        tags = sorted(set(ep.tag for ep in self.endpoints))
        
        for tag in tags:
            tag_endpoints = [ep for ep in self.endpoints if ep.tag == tag]
            safe_tag = self._make_safe_name(tag)
            
            lines.append(f"### {tag}")
            lines.append("")
            
            for endpoint in tag_endpoints:
                lines.append(f"#### `{self.config.entry_point} {safe_tag} {endpoint.name}`")
                lines.append("")
                lines.append(f"- **HTTP 方法**: {endpoint.method}")
                lines.append(f"- **路径**: `{endpoint.path}`")
                lines.append(f"- **描述**: {endpoint.summary}")
                
                if endpoint.description:
                    lines.append("")
                    lines.append(f"{endpoint.description}")
                
                if endpoint.parameters:
                    lines.append("")
                    lines.append("**参数**:")
                    lines.append("")
                    lines.append("| 名称 | 位置 | 类型 | 必需 | 描述 |")
                    lines.append("|------|------|------|------|------|")
                    for param in endpoint.parameters:
                        req = "是" if param["required"] else "否"
                        default = param.get("default")
                        desc = param["description"]
                        if default is not None:
                            desc += f" (默认: {default})"
                        lines.append(f"| {param['name']} | {param['in']} | {param['type']} | {req} | {desc} |")
                
                if endpoint.request_body:
                    lines.append("")
                    lines.append("**请求体**: JSON 格式")
                
                lines.append("")
                lines.append("**示例**:")
                lines.append("")
                lines.append("```bash")
                
                # 构建示例命令
                cmd_parts = [self.config.entry_point, safe_tag, endpoint.name]
                
                # 添加路径参数示例
                for param in endpoint.parameters:
                    if param["in"] == "path":
                        cmd_parts.append(f"{param['name']}")
                
                # 添加查询参数示例
                query_params = [p for p in endpoint.parameters if p["in"] == "query"]
                for param in query_params[:2]:  # 只显示前2个作为示例
                    if param["type"] == "str":
                        cmd_parts.append(f"--{param['name']} 'value'")
                    else:
                        cmd_parts.append(f"--{param['name']} 123")
                
                # 添加请求体示例
                if endpoint.request_body:
                    cmd_parts.append("--data '{\"key\": \"value\"}'")
                
                lines.append(" ".join(cmd_parts))
                lines.append("```")
                lines.append("")
        
        return "\n".join(lines)
    
    def _make_safe_name(self, name: str) -> str:
        """将名称转换为安全的标识符"""
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        if safe and safe[0].isdigit():
            safe = '_' + safe
        return safe.lower()


class FastAPIToCLI:
    """FastAPI 转 CLI 主类"""
    
    def __init__(self, config: CLIGeneratorConfig):
        self.config = config
        self.endpoints: List[EndpointInfo] = []
    
    def generate_from_spec(self, openapi_spec: Dict[str, Any]) -> str:
        """从 OpenAPI 规范生成 CLI 代码"""
        parser = OpenAPIParser(openapi_spec)
        self.endpoints = parser.parse_endpoints(self.config)
        
        generator = TyperCLIGenerator(self.endpoints, self.config)
        return generator.generate()
    
    def generate_from_file(self, spec_file: Union[str, Path]) -> str:
        """从 OpenAPI JSON 文件生成 CLI 代码"""
        spec_path = Path(spec_file)
        if not spec_path.exists():
            raise FileNotFoundError(f"找不到文件: {spec_path}")
        
        openapi_spec = json.loads(spec_path.read_text(encoding='utf-8'))
        return self.generate_from_spec(openapi_spec)
    
    def generate_from_app(self, app) -> str:
        """从 FastAPI 应用实例生成 CLI 代码"""
        if not hasattr(app, "openapi"):
            raise ValueError("提供的对象不是有效的 FastAPI 应用")
        
        openapi_spec = app.openapi()
        return self.generate_from_spec(openapi_spec)
    
    def generate_setup_py(self) -> str:
        """生成 setup.py 内容"""
        generator = SetupPyGenerator(self.config)
        return generator.generate()
    
    def generate_markdown(self) -> str:
        """生成 Markdown 文档"""
        if not self.endpoints:
            raise ValueError("还没有生成端点信息，请先调用 generate_from_app 或 generate_from_spec")
        
        generator = MarkdownDocGenerator(self.endpoints, self.config)
        return generator.generate()
    
    def save_files(self, cli_code: str, output_dir: Optional[Path] = None) -> Dict[str, Path]:
        """保存所有生成的文件"""
        output_dir = Path(output_dir or self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = {}
        
        # 保存 CLI 文件
        cli_path = output_dir / self.config.output_file
        cli_path.write_text(cli_code, encoding='utf-8')
        cli_path.chmod(0o755)
        saved_files['cli'] = cli_path
        
        # 保存 setup.py
        if self.config.generate_setup_py:
            setup_code = self.generate_setup_py()
            setup_path = output_dir / "setup.py"
            setup_path.write_text(setup_code, encoding='utf-8')
            saved_files['setup'] = setup_path
        
        # 保存 Markdown 文档
        if self.config.generate_markdown:
            markdown_code = self.generate_markdown()
            markdown_path = output_dir / f"{self.config.name}-cli.md"
            markdown_path.write_text(markdown_code, encoding='utf-8')
            saved_files['markdown'] = markdown_path
        
        return saved_files


def load_fastapi_app(module_path: str, app_var: str = "app"):
    """从文件加载 FastAPI 应用"""
    if ":" in module_path:
        file_path, app_var = module_path.split(":")
    else:
        file_path = module_path
        app_var = "app"
    
    if not file_path.endswith(".py"):
        file_path += ".py"
    
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"找不到文件: {file_path}")
    
    spec = importlib.util.spec_from_file_location("fastapi_module", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["fastapi_module"] = module
    spec.loader.exec_module(module)
    
    if not hasattr(module, app_var):
        raise AttributeError(f"模块中找不到变量: {app_var}")
    
    return getattr(module, app_var)


def generate_cli_project(
    config: CLIGeneratorConfig,
    output_dir: Optional[Path] = None
) -> Dict[str, Path]:
    """
    生成完整的 CLI 项目
    
    Args:
        config: 生成器配置
        output_dir: 输出目录，默认为配置中的 output_dir
    
    Returns:
        生成的文件路径字典
    """
    output_dir = output_dir or Path(config.output_dir)
    
    # 加载 FastAPI 应用
    app = load_fastapi_app(config.fastapi_module)
    
    # 生成 CLI
    converter = FastAPIToCLI(config)
    cli_code = converter.generate_from_app(app)
    
    # 保存所有文件
    saved_files = converter.save_files(cli_code, output_dir)
    
    return saved_files
