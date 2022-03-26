from typing import Optional, List

from pydantic import Field

from src.models.mongo_model import MongoModel, OID


class Product(MongoModel):
    id: OID = Field(alias='_id')
    image: Optional[List[str]]
    description: str
    price: float
