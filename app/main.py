from fastapi import FastAPI
from routes import auth, transactions
import uvicorn

from routes import auth, transactions

app = FastAPI()

app.include_router(auth.router, tags=["Authentication"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)