from sqlalchemy import Column, Integer, String
from database.config.database import Base


class ProductInfo(Base):
    __tablename__ = "product_info"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    productName = Column(String)
    description = Column(String)
    code = Column(String, unique=True)
    price = Column(String)
