from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.database import Base, engine

# Create the FastAPI app instance
app = FastAPI(title="User Authentication Service")

# Add CORS middleware (optional, enable if you plan to allow cross-origin requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router for the authentication endpoints
app.include_router(router)

# Create the database tables
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Optionally add a root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the User Authentication Service!"}

# Run the app with: poetry run uvicorn app.main:app --reload
