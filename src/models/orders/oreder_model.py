from typing import Optional
from uuid import uuid4

from pydantic import Field

from src.models.mongo_model import MongoModel, OID
from src.models.products.product_model import Product
from src.models.users.user_model import UserOut


class Order(MongoModel):
    id: Optional[OID] = Field(alias='_id')
    order_id: Optional[str] = 'ID_' + str(uuid4()).replace('-', '')
    product: OID
    quantity: int
    user: Optional[OID]


class OrderOut(MongoModel):
    id: Optional[OID] = Field(alias='_id')
    order_id: Optional[str] = 'ID_' + str(uuid4()).replace('-', '')
    product: Product
    quantity: int
    user: UserOut