from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Revision(Base):
    __tablename__ = "revisions"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    content = Column(Text)
    edited_by = Column(Integer, ForeignKey("users.id"))
    edited_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(String)

    article = relationship("Article", back_populates="revisions")
