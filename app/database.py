from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import Base as UserBase
from app.models.transaction import Base as TransactionBase

DATABASE_URL = "mysql+mysqlconnector://root:rootpassword@localhost/finance_db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц в базе данных
UserBase.metadata.create_all(bind=engine)
TransactionBase.metadata.create_all(bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()