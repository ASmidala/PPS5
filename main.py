import jwt
import datetime
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- DATABASE SETUP ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./pps_data.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)

Base.metadata.create_all(bind=engine)

# --- APP SETUP ---
app = FastAPI()
security = HTTPBearer()
SECRET_KEY = "a-very-long-secret-key-that-is-secure-for-production"

# --- AI CONTROLLER ---
class AIAgent:
    def process(self, intent: str):
        if "analyze" in intent.lower():
            return {"status": "success", "result": "Pyramid Analysis Pulse Active"}
        return {"status": "error", "message": "Intent not recognized"}

agent = AIAgent()

# --- AUTH & ROUTES ---
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        return jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/login")
def login():
    token = jwt.encode({"sub": "admin", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY)
    return {"access_token": token}

@app.post("/orchestrate")
async def orchestrate(data: dict, token: dict = Depends(verify_token)):
    return agent.process(data.get("intent", ""))

# Mount Frontend
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")