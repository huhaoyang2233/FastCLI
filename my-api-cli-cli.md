# my-api-cli

由 FastAPI 自动生成的 CLI 工具

- **版本**: 1.0.0
- **API 基础 URL**: http://localhost:8000
- **CLI 命令**: `mytool`

## 安装

```bash
pip install -e .
```

## 使用

安装后，可以使用 `mytool` 命令来访问 API。

## 命令列表

### products

#### `mytool products list_products`

- **HTTP 方法**: GET
- **路径**: `/products`
- **描述**: List Products

Get all products

**参数**:

| 名称 | 位置 | 类型 | 必需 | 描述 |
|------|------|------|------|------|
| skip | query | int | 否 |  (默认: 0) |
| limit | query | int | 否 |  (默认: 10) |

**示例**:

```bash
mytool products list_products --skip 123 --limit 123
```

#### `mytool products get_products_by_id`

- **HTTP 方法**: GET
- **路径**: `/products/{product_id}`
- **描述**: Get Product

Get a product by ID

**参数**:

| 名称 | 位置 | 类型 | 必需 | 描述 |
|------|------|------|------|------|
| product_id | path | int | 是 |  |

**示例**:

```bash
mytool products get_products_by_id product_id
```

### system

#### `mytool system list_health`

- **HTTP 方法**: GET
- **路径**: `/health`
- **描述**: Health Check

Health check

**示例**:

```bash
mytool system list_health
```

### users

#### `mytool users list_users`

- **HTTP 方法**: GET
- **路径**: `/users`
- **描述**: List Users

Get all users

**参数**:

| 名称 | 位置 | 类型 | 必需 | 描述 |
|------|------|------|------|------|
| skip | query | int | 否 |  (默认: 0) |
| limit | query | int | 否 |  (默认: 10) |

**示例**:

```bash
mytool users list_users --skip 123 --limit 123
```

#### `mytool users create_users`

- **HTTP 方法**: POST
- **路径**: `/users`
- **描述**: Create User

Create a new user

**请求体**: JSON 格式

**示例**:

```bash
mytool users create_users --data '{"key": "value"}'
```

#### `mytool users get_users_by_id`

- **HTTP 方法**: GET
- **路径**: `/users/{user_id}`
- **描述**: Get User

Get a user by ID

**参数**:

| 名称 | 位置 | 类型 | 必需 | 描述 |
|------|------|------|------|------|
| user_id | path | int | 是 |  |

**示例**:

```bash
mytool users get_users_by_id user_id
```
