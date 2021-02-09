from sqlalchemy import Column, Integer, String, Boolean
from database.config.database import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    fullName = Column(String)
    admin = Column(Boolean)
