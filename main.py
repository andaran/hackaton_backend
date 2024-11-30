from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, inspect
from models import User, get_user_transaction_table
from database import get_db, engine
from schemas import UserCreate, UserLogin, TransactionCreate, TransactionOut
import uvicorn

app = FastAPI()

@app.post("/login/")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.password == user.password).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    cleaned_user = {
        "id": db_user.id,
        "email": db_user.email,
        "name": db_user.name
    }
    return {
        "message": "Login successful",
        "user": cleaned_user
    }

@app.post("/register/")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, password=user.password, name=user.name)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/transactions/{user_id}/", response_model=TransactionOut)
async def add_transaction(user_id: str, transaction: TransactionCreate, db: Session = Depends(get_db)):
    metadata = MetaData()
    Transaction = get_user_transaction_table(user_id, metadata)

    # Проверка существования пользователя
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Валидация типа транзакции
    if transaction.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    # Создание таблицы, если она не существует
    if not inspect(engine).has_table(Transaction.__tablename__):
        Transaction.__table__.create(bind=engine)

    # Добавляем транзакцию в таблицу
    db_transaction = Transaction(
        date=transaction.date,
        type=transaction.type,
        category=transaction.category,
        place=transaction.place,
        amount=transaction.amount,
        description=transaction.description
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/{user_id}/", response_model=list[TransactionOut])
async def get_transactions(user_id: str, db: Session = Depends(get_db)):
    metadata = MetaData()
    Transaction = get_user_transaction_table(user_id, metadata)

    # Если таблица не существует, то возвращаем ошибку
    if not inspect(engine).has_table(Transaction.__tablename__):
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    transactions = db.query(Transaction).all()
    return transactions

@app.delete("/transactions/{user_id}/{transaction_id}/")
async def delete_transaction(user_id: str, transaction_id: int, db: Session = Depends(get_db)):
    metadata = MetaData()
    Transaction = get_user_transaction_table(user_id, metadata)

    # Если таблица не существует, то возвращаем ошибку
    if not inspect(engine).has_table(Transaction.__tablename__):
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

@app.get("/transactions/{user_id}/{start_date}/{end_date}/", response_model=list[TransactionOut])
async def get_transactions_by_period(user_id: str, start_date: str, 
                                     end_date: str, db: Session = Depends(get_db)):
    metadata = MetaData()
    Transaction = get_user_transaction_table(user_id, metadata)

    # Если таблица не существует, то возвращаем ошибку
    if not inspect(engine).has_table(Transaction.__tablename__):
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    transactions = db.query(Transaction).filter(
        Transaction.date >= start_date, Transaction.date <= end_date).all()
    transactions = sorted(transactions, key=lambda x: x.date)

    return transactions

if __name__ == "__main__":
    uvicorn.run(app, port=8000)