#!/usr/bin/env python3
"""
由 FastAPI 自动生成的 CLI 工具
由 FastAPI 服务自动生成
"""

import json
from typing import Optional, List
import typer
import requests
from rich.console import Console
from rich.table import Table
from rich import print as rprint


BASE_URL = "http://localhost:8000"

# 初始化
app = typer.Typer(help='由 FastAPI 自动生成的 CLI 工具', add_completion=False)
console = Console()

products_app = typer.Typer(help='products 相关命令')
system_app = typer.Typer(help='system 相关命令')
users_app = typer.Typer(help='users 相关命令')

app.add_typer(products_app, name='products')
app.add_typer(system_app, name='system')
app.add_typer(users_app, name='users')

@products_app.command(name='list_products', help='''List Products''')
def list_products(skip: Optional[int] = typer.Option(0, help=''), limit: Optional[int] = typer.Option(10, help='')):
    """Get all products"""
    try:
        url = f"{BASE_URL}/products"
        params = {}
        if skip is not None:
            params['skip'] = skip
        if limit is not None:
            params['limit'] = limit

        response = requests.get(url, params=params)

        if response.status_code in [200, 201, 202]:
            result = response.json()
            if isinstance(result, list):
                if result:
                    table = Table(show_header=True, header_style='bold magenta')
                    for key in result[0].keys():
                        table.add_column(str(key))
                    for item in result:
                        table.add_row(*[str(v) for v in item.values()])
                    console.print(table)
                else:
                    rprint('[yellow]暂无数据[/yellow]')
            else:
                table = Table(show_header=True, header_style='bold green')
                table.add_column('字段')
                table.add_column('值')
                for key, value in result.items():
                    table.add_row(str(key), str(value))
                console.print(table)
        else:
            rprint(f'[red]请求失败: {response.status_code}[/red]')
            rprint(response.text)

    except Exception as e:
        rprint(f'[red]错误: {e}[/red]')
        raise typer.Exit(1)

@products_app.command(name='get_products_by_id', help='''Get Product''')
def get_products_by_id(product_id: int):
    """Get a product by ID"""
    try:
        url = f"{BASE_URL}/products/{product_id}"
        response = requests.get(url)

        if response.status_code in [200, 201, 202]:
            result = response.json()
            if isinstance(result, list):
                if result:
                    table = Table(show_header=True, header_style='bold magenta')
                    for key in result[0].keys():
                        table.add_column(str(key))
                    for item in result:
                        table.add_row(*[str(v) for v in item.values()])
                    console.print(table)
                else:
                    rprint('[yellow]暂无数据[/yellow]')
            else:
                table = Table(show_header=True, header_style='bold green')
                table.add_column('字段')
                table.add_column('值')
                for key, value in result.items():
                    table.add_row(str(key), str(value))
                console.print(table)
        else:
            rprint(f'[red]请求失败: {response.status_code}[/red]')
            rprint(response.text)

    except Exception as e:
        rprint(f'[red]错误: {e}[/red]')
        raise typer.Exit(1)

@system_app.command(name='list_health', help='''Health Check''')
def list_health():
    """Health check"""
    try:
        url = f"{BASE_URL}/health"
        response = requests.get(url)

        if response.status_code in [200, 201, 202]:
            result = response.json()
            if isinstance(result, list):
                if result:
                    table = Table(show_header=True, header_style='bold magenta')
                    for key in result[0].keys():
                        table.add_column(str(key))
                    for item in result:
                        table.add_row(*[str(v) for v in item.values()])
                    console.print(table)
                else:
                    rprint('[yellow]暂无数据[/yellow]')
            else:
                table = Table(show_header=True, header_style='bold green')
                table.add_column('字段')
                table.add_column('值')
                for key, value in result.items():
                    table.add_row(str(key), str(value))
                console.print(table)
        else:
            rprint(f'[red]请求失败: {response.status_code}[/red]')
            rprint(response.text)

    except Exception as e:
        rprint(f'[red]错误: {e}[/red]')
        raise typer.Exit(1)

@users_app.command(name='list_users', help='''List Users''')
def list_users(skip: Optional[int] = typer.Option(0, help=''), limit: Optional[int] = typer.Option(10, help='')):
    """Get all users"""
    try:
        url = f"{BASE_URL}/users"
        params = {}
        if skip is not None:
            params['skip'] = skip
        if limit is not None:
            params['limit'] = limit

        response = requests.get(url, params=params)

        if response.status_code in [200, 201, 202]:
            result = response.json()
            if isinstance(result, list):
                if result:
                    table = Table(show_header=True, header_style='bold magenta')
                    for key in result[0].keys():
                        table.add_column(str(key))
                    for item in result:
                        table.add_row(*[str(v) for v in item.values()])
                    console.print(table)
                else:
                    rprint('[yellow]暂无数据[/yellow]')
            else:
                table = Table(show_header=True, header_style='bold green')
                table.add_column('字段')
                table.add_column('值')
                for key, value in result.items():
                    table.add_row(str(key), str(value))
                console.print(table)
        else:
            rprint(f'[red]请求失败: {response.status_code}[/red]')
            rprint(response.text)

    except Exception as e:
        rprint(f'[red]错误: {e}[/red]')
        raise typer.Exit(1)

@users_app.command(name='create_users', help='''Create User''')
def create_users(data: Optional[str] = typer.Option(None, help='请求体 JSON 字符串')):
    """Create a new user"""
    try:
        url = f"{BASE_URL}/users"
        # 解析请求体
        json_data = json.loads(data) if data else None
        response = requests.post(url, json=json_data)

        if response.status_code in [200, 201, 202]:
            result = response.json()
            if isinstance(result, list):
                if result:
                    table = Table(show_header=True, header_style='bold magenta')
                    for key in result[0].keys():
                        table.add_column(str(key))
                    for item in result:
                        table.add_row(*[str(v) for v in item.values()])
                    console.print(table)
                else:
                    rprint('[yellow]暂无数据[/yellow]')
            else:
                table = Table(show_header=True, header_style='bold green')
                table.add_column('字段')
                table.add_column('值')
                for key, value in result.items():
                    table.add_row(str(key), str(value))
                console.print(table)
        else:
            rprint(f'[red]请求失败: {response.status_code}[/red]')
            rprint(response.text)

    except Exception as e:
        rprint(f'[red]错误: {e}[/red]')
        raise typer.Exit(1)

@users_app.command(name='get_users_by_id', help='''Get User''')
def get_users_by_id(user_id: int):
    """Get a user by ID"""
    try:
        url = f"{BASE_URL}/users/{user_id}"
        response = requests.get(url)

        if response.status_code in [200, 201, 202]:
            result = response.json()
            if isinstance(result, list):
                if result:
                    table = Table(show_header=True, header_style='bold magenta')
                    for key in result[0].keys():
                        table.add_column(str(key))
                    for item in result:
                        table.add_row(*[str(v) for v in item.values()])
                    console.print(table)
                else:
                    rprint('[yellow]暂无数据[/yellow]')
            else:
                table = Table(show_header=True, header_style='bold green')
                table.add_column('字段')
                table.add_column('值')
                for key, value in result.items():
                    table.add_row(str(key), str(value))
                console.print(table)
        else:
            rprint(f'[red]请求失败: {response.status_code}[/red]')
            rprint(response.text)

    except Exception as e:
        rprint(f'[red]错误: {e}[/red]')
        raise typer.Exit(1)


def main():
    app()

if __name__ == '__main__':
    main()