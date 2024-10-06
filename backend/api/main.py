from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine  
from routers import auth, workouts, routines

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"message": "Health check OK"}

app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(routines.router)
