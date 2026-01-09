from fastapi import FastAPI
from app.routes import book

app = FastAPI(debug=True)
from app.routes.auth import router as auth_router

app.include_router(auth_router)

# app.include_router(auth.router)
app.include_router(book.router)

