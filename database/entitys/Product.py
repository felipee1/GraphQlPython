from graphene_sqlalchemy import SQLAlchemyObjectType
from database.models.ProductModel import ProductInfo
from pydantic import BaseModel


class ProductInfoBase(BaseModel):
    productName: str


class ProductCreate(ProductInfoBase):
    description: str
    code: str
    price: str
    userId: int


class ProductInformation(ProductInfoBase):
    id: int

    class Config:
        orm_mode = True


class ProductInfoSchema(SQLAlchemyObjectType):
    class Meta:
        model = ProductInfo
