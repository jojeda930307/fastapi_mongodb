from typing import Optional

from pydantic import Field

from src.models.address.address_model import UserAddress
from src.models.mongo_model import MongoModel, OID


class UserIn(MongoModel):
    id: Optional[OID] = Field(alias='_id')
    name: str = Field()
    email: str = Field()
    password: str = Field()


class UserOut(MongoModel):
    id: OID = Field(alias='_id')
    name: str
    email: str
    address: Optional[UserAddress]