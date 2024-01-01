# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.routers import auth,domain
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates


load_dotenv()
app = FastAPI()

templates = Jinja2Templates(directory="templates")
origins=["http://localhost:3000","http://127.0.0.1:3000"]

# CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
   allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(domain.router,prefix='/domain',tags=['domain'])


