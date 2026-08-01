# PPS_Global_Unified.py
# ---------------------------------------------------------
# Consolidated Application Scaffold for PPS Global
# ---------------------------------------------------------

import jwt
import datetime
import requests
from fastapi import FastAPI, HTTPException, Security, Depends
# Ensure these are imported from fastapi.security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI()
security = HTTPBearer()

from fastapi.staticfiles import StaticFiles

# Add this after app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")

# --- 1. AUTHENTICATION MODULE ---
SECRET_KEY = "your-very-secure-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        return jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- 2. AI AGENT CONTROLLER (The Brain) ---
class AIAgentController:
    def __init__(self):
        self.name = "PPS AI Core"

    async def process_intent(self, intent: str):
        if "analyze" in intent:
            return {"status": "success", "data": "Pyramid Analysis Pulse Active"}
        return {"status": "error", "message": "Intent not recognized"}

agent = AIAgentController()

# --- 3. API ROUTES (The Interface) ---
class Query(BaseModel):
    intent: str

@app.post("/api/v1/orchestrate")
async def orchestrate(query: Query, token: dict = Depends(verify_token)):
    result = await agent.process_intent(query.intent)
    return result

@app.get("/health")
async def health():
    return {"status": "PPS Global System Online"}

@app.get("/login")
def login():
    token = create_access_token({"sub": "admin"})
    return {"access_token": token}

# --- 4. DEPLOYMENT HOOKS ---
# Run with: uvicorn PPS_Global_Unified:app --reload