from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status, HTTPException
from models import Workout
from deps import db_dependency, user_dependency

router = APIRouter(prefix="/workouts", tags=["workouts"])

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    pass

@router.get("/", status_code=status.HTTP_200_OK)
async def get_workout(user: user_dependency, db: db_dependency, workout_id: int):
    return db.query(Workout).filter(Workout.id == workout_id).first()

@router.get('/workouts', status_code=status.HTTP_200_OK)
async def get_all_workouts(user: user_dependency, db: db_dependency):
    return db.query(Workout).all()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_workout(user: user_dependency, db: db_dependency, workout_request: WorkoutCreate):
    db_workout = Workout(**workout_request.model_dump(), user_id=user.get("id"))
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.delete('/', status_code=status.HTTP_200_OK)
async def delete_workout(user: user_dependency, db: db_dependency, workout_id: int):
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    db.delete(db_workout)
    db.commit()
    return db_workout
