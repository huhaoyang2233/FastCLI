"""FastAPI Example Service"""
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Path, Query, HTTPException

app = FastAPI(
    title="Example API Service",
    description="A demo service for FastAPI to CLI conversion",
    version="1.0.0"
)


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None


class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True


users_db = {
    1: User(id=1, name="Alice", email="alice@example.com", age=25),
    2: User(id=2, name="Bob", email="bob@example.com", age=30),
}

products_db = {
    1: Product(id=1, name="Laptop", price=999.0, description="High performance", in_stock=True),
    2: Product(id=2, name="Mouse", price=29.0, in_stock=True),
}


@app.get("/users", response_model=List[User], tags=["users"])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Get all users"""
    user_list = list(users_db.values())
    return user_list[skip: skip + limit]


@app.get("/users/{user_id}", response_model=User, tags=["users"])
async def get_user(user_id: int = Path(..., ge=1)):
    """Get a user by ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.post("/users", response_model=User, tags=["users"])
async def create_user(user: UserCreate):
    """Create a new user"""
    new_id = max(users_db.keys()) + 1 if users_db else 1
    new_user = User(id=new_id, **user.model_dump())
    users_db[new_id] = new_user
    return new_user


@app.get("/products", response_model=List[Product], tags=["products"])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Get all products"""
    product_list = list(products_db.values())
    return product_list[skip: skip + limit]


@app.get("/products/{product_id}", response_model=Product, tags=["products"])
async def get_product(product_id: int = Path(..., ge=1)):
    """Get a product by ID"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]


@app.get("/health", tags=["system"])
async def health_check():
    """Health check"""
    return {"status": "healthy"}
