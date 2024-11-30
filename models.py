from sqlalchemy import Column, Integer, String, Float, Date, Enum, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    name = Column(String(255))

class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"

def get_user_transaction_table(user_id: str, metadata: MetaData):
    """
    Динамическая генерация таблицы транзакций для каждого пользователя
    """
    class Transaction(Base):
        __tablename__ = f"transactions_{user_id}"
        __table__ = Table(
            f"transactions_{user_id}", metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('date', Date, nullable=False),
            Column('type', Enum(TransactionType), nullable=False),
            Column('category', String(100), nullable=False),
            Column('place', String(100), nullable=False),
            Column('amount', Float, nullable=False),
            Column('description', String(255), nullable=True),
        )
    return Transaction