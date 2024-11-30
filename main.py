from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import UserCreate, UserLogin
import uvicorn

app = FastAPI()

@app.post("/login/")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.password == user.password).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"message": "Login successful"}

@app.post("/register/")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, password=user.password, name=user.name)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)