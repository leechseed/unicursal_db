from .database import SessionLocal, engine, Base
from .models import User

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    print("✅ User added successfully.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()
