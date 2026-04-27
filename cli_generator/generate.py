#!/usr/bin/env python3
"""
FastAPI 转 CLI 生成器 - 启动脚本

这个脚本读取 config.json 配置文件，生成 CLI 工具、setup.py 和 Markdown 文档。
所有生成结果放在与 FastAPI 启动文件同级的目录下。

使用方法:
    python cli_generator/generate.py
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from generator import CLIGeneratorConfig, generate_cli_project


def main():
    """主函数"""
    print("🚀 FastAPI 转 CLI 生成器")
    print("=" * 60)
    
    # 配置文件路径（在 cli_generator 目录下）
    config_file = Path(__file__).parent / "config.json"
    
    if not config_file.exists():
        print(f"❌ 找不到配置文件: {config_file}")
        print("\n请创建 config.json 配置文件:")
        print("""
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
  },
  "output": {
    "output_dir": "."
  }
}
""")
        return 1
    
    try:
        # 从 JSON 加载配置
        print(f"📄 加载配置文件: {config_file}")
        config = CLIGeneratorConfig.from_json(config_file)
        
        # 确定 FastAPI 模块路径
        fastapi_file = config.fastapi_module.split(":")[0]
        if not fastapi_file.endswith(".py"):
            fastapi_file += ".py"
        
        # 确定输出目录 (与 FastAPI 文件同级)
        fastapi_path = Path(fastapi_file)
        if fastapi_path.exists():
            output_dir = fastapi_path.parent
        else:
            output_dir = Path(config.output_dir)
        
        print(f"📦 FastAPI 模块: {config.fastapi_module}")
        print(f"📂 输出目录: {output_dir.absolute()}")
        print(f"⚙️  配置:")
        print(f"   - 包名: {config.name}")
        print(f"   - 版本: {config.version}")
        print(f"   - CLI 命令: {config.entry_point}")
        print(f"   - CLI 文件: {config.output_file}")
        print()
        
        # 生成 CLI 项目
        saved_files = generate_cli_project(config, output_dir)
        
