from typing import Optional, List
from sqlmodel import Field, SQLModel, Column
from pgvector.sqlalchemy import Vector

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    price: float
    description: str
    inventory_count: int = Field(default=0)
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(Vector(384)))