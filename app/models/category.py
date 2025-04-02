from sqlalchemy import Column, Integer, String, ForeignKey, Table
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
