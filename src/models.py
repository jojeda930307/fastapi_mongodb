from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from bson import ObjectId
from pydantic import BaseModel, Field, BaseConfig


class OID(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class UserAddress(MongoModel):
    id: Optional[OID] = Field(alias='_id')
    city: str = Field()
    location: str = Field()
    street: str = Field()
    flat: int = Field()
    door: str = Field()
    postal_code: int = Field()


class UserIn(MongoModel):
    id: Optional[OID] = Field(alias='_id')
    name: str = Field()
    email: str = Field()
    password: str = Field()
    created_at: Optional[datetime] = datetime.now()


class UserInDB(MongoModel):
    """ To save credentials in database this most be encrypted """
    pass


class Product(MongoModel):
    id: OID = Field(alias='_id')
    image: Optional[List[str]]
    description: str
    price: float


class Order(MongoModel):
    id: Optional[OID] = Field(alias='_id')
    order_id: Optional[str] = 'ID_' + str(uuid4()).replace('-', '')
    product: OID
    quantity: int
    user: Optional[OID]


class UserOut(MongoModel):
    id: OID = Field(alias='_id')
    name: str
    email: str
    address: Optional[OID]
    created_at: datetime


class OrderOut(MongoModel):
    id: Optional[OID] = Field(alias='_id')
    order_id: Optional[str] = 'ID_' + str(uuid4()).replace('-', '')
    product: Product
    quantity: int
    user: UserOut
