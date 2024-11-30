from fastapi import FastAPI
from app.routes import auth, transactions
import uvicorn

from app.routes import auth, transactions

app = FastAPI()

app.include_router(auth.router, tags=["Authentication"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

if __name__ == "__main__":
    uvicorn.run(app, port=8000)