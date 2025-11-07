from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from pets import router as pets_router
from database import init_db
from auth import router as auth_router # <-- We import our router
from vets import router as vets_router
from health import router as health_router
from reminders import router as reminders_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    await init_db()
    yield
    # Code to run on shutdown (if any)
    print("Server shutting down...")


# Create the FastAPI app instance
app = FastAPI(title="PetPal API", lifespan=lifespan)

# --- 1. DEFINE CORS ORIGINS ---
# Let's make this list more robust
origins = [
    "http://localhost:8100",  # Ionic app on localhost
    "http://127.0.0.1:8100", # Ionic app on 127.0.0.1
    "http://localhost",
]

# --- 2. ADD MIDDLEWARE (MUST BE BEFORE ROUTERS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Which origins are allowed
    allow_credentials=True,    # Allow cookies/auth headers
    allow_methods=["*"],       # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],       # Allow all headers
)

# --- 3. INCLUDE ROUTERS (MUST BE AFTER MIDDLEWARE) ---
app.include_router(auth_router)
app.include_router(pets_router)
app.include_router(vets_router)
app.include_router(health_router)
app.include_router(reminders_router)
# --- Test Endpoint ---
@app.get("/")
async def root():
    return {"message": "Welcome to the PetPal API! Database is connected."}


# This part is for running with 'python main.py'
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)