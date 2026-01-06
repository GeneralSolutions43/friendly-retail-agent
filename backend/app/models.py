from typing import Optional, List
from sqlmodel import Field, SQLModel, Column
from pgvector.sqlalchemy import Vector
from sqlalchemy import event
from .embeddings import get_embedding

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    price: float
    description: str
    inventory_count: int = Field(default=0)
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(Vector(384)), exclude=True)

    def update_embedding(self):
        """Generates and updates the embedding for the product."""
        # Combine relevant fields for semantic search
        text_to_embed = f"{self.name}: {self.description}"
        self.embedding = get_embedding(text_to_embed)

# Register event listeners to automatically update embedding on save
@event.listens_for(Product, "before_insert")
@event.listens_for(Product, "before_update")
def receive_before_insert_or_update(mapper, connection, target):
    target.update_embedding()
