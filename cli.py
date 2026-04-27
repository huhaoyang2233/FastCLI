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

default_app = typer.Typer(help='default 相关命令')

app.add_typer(default_app, name='default')

@default_app.command(name='list_users', help='''获取用户列表''')
def list_users(skip: Optional[int] = typer.Option(0, help='跳过的记录数'), limit: Optional[int] = typer.Option(10, help='返回的最大记录数')):
    """获取所有用户的列表，支持分页"""
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

@default_app.command(name='create_users', help='''创建用户''')
def create_users(data: Optional[str] = typer.Option(None, help='请求体 JSON 字符串')):
    """创建一个新用户"""
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

@default_app.command(name='get_users_by_id', help='''获取单个用户''')
def get_users_by_id(user_id: int):
    """根据用户ID获取单个用户信息"""
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

@default_app.command(name='update_users_by_id', help='''更新用户''')
def update_users_by_id(user_id: int, data: Optional[str] = typer.Option(None, help='请求体 JSON 字符串')):
    """根据用户ID更新用户信息"""
    try:
        url = f"{BASE_URL}/users/{user_id}"
        # 解析请求体
        json_data = json.loads(data) if data else None
        response = requests.put(url, json=json_data)

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

@default_app.command(name='delete_users_by_id', help='''删除用户''')
def delete_users_by_id(user_id: int):
    """根据用户ID删除用户"""
    try:
        url = f"{BASE_URL}/users/{user_id}"
        response = requests.delete(url)

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

@default_app.command(name='list_products', help='''获取商品列表''')
def list_products(skip: Optional[int] = typer.Option(0, help='跳过的记录数'), limit: Optional[int] = typer.Option(10, help='返回的最大记录数'), in_stock_only: Optional[bool] = typer.Option(False, help='是否只显示有库存的商品')):
    """获取所有商品的列表，支持分页和库存筛选"""
    try:
        url = f"{BASE_URL}/products"
        params = {}
        if skip is not None:
            params['skip'] = skip
        if limit is not None:
            params['limit'] = limit
        if in_stock_only is not None:
            params['in_stock_only'] = in_stock_only

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

@default_app.command(name='create_products', help='''创建商品''')
def create_products(data: Optional[str] = typer.Option(None, help='请求体 JSON 字符串')):
    """创建一个新商品"""
    try:
        url = f"{BASE_URL}/products"
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

@default_app.command(name='get_products_by_id', help='''获取单个商品''')
def get_products_by_id(product_id: int):
    """根据商品ID获取单个商品信息"""
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

@default_app.command(name='update_products_by_id', help='''更新商品''')
def update_products_by_id(product_id: int, data: Optional[str] = typer.Option(None, help='请求体 JSON 字符串')):
    """根据商品ID更新商品信息"""
    try:
        url = f"{BASE_URL}/products/{product_id}"
        # 解析请求体
        json_data = json.loads(data) if data else None
        response = requests.put(url, json=json_data)

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

@default_app.command(name='delete_products_by_id', help='''删除商品''')
def delete_products_by_id(product_id: int):
    """根据商品ID删除商品"""
    try:
        url = f"{BASE_URL}/products/{product_id}"
        response = requests.delete(url)

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

@default_app.command(name='list_health', help='''健康检查''')
def list_health():
    """检查服务是否正常运行"""
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

@default_app.command(name='get_root', help='''根路径''')
def get_root():
    """API 根路径，返回基本信息"""
    try:
        url = f"{BASE_URL}/"
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