from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

# Перечисление для типа транзакции
class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

# Pydantic схема для добавления транзакции
class TransactionCreate(BaseModel):
    date: date
    type: TransactionType
    category: str
    place: str
    amount: float
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Pydantic схема для транзакции (для вывода)
class TransactionOut(TransactionCreate):
    id: int

    class Config:
        orm_mode = True