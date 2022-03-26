from typing import Optional

from pydantic import Field

from src.models.mongo_model import MongoModel, OID


class UserAddress(MongoModel):
    id: Optional[OID] = Field(alias='_id')
    city: str = Field()
    location: str = Field()
    street: str = Field()
    flat: int = Field()
    door: str = Field()
    postal_code: int = Field()


class UserAddressOut(MongoModel):
    city: str = Field()
    location: str = Field()
    street: str = Field()
    flat: int = Field()
    door: str = Field()
    postal_code: int = Field()
