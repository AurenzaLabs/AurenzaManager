from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

try:
    from backend.database import users_col
    from backend.auth import verify_password, create_token
    from backend.routes import users, projects, expenses, pnl
except ModuleNotFoundError:
    from database import users_col
    from auth import verify_password, create_token
    from routes import users, projects, expenses, pnl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(expenses.router)
app.include_router(pnl.router)

@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        user = users_col.find_one({"email": email})
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")

    if not user or not verify_password(password, user.get("password", "")):
        raise HTTPException(status_code=401)
    
    token = create_token({
        "user_id": str(user["_id"]),
        "role": user["role"]
    })
    return {"token": token, "role": user["role"]}
