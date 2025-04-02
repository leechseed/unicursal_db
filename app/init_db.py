from app.database import engine
from app.models.base import Base
from app.models import User, Article, Revision, Category

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
