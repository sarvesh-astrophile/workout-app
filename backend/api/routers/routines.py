from pydantic import BaseModel
from typing import Optional, List
from models import Routine, Workout
from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import joinedload
from deps import db_dependency, user_dependency

router = APIRouter(prefix="/routines", tags=["routines"])

class RoutineBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoutineCreate(RoutineBase):
    workouts: List[int] = []

@router.get("/", status_code=status.HTTP_200_OK)
async def get_routines(user: user_dependency, db: db_dependency):
    return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id == user.get("id")).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_routine(user: user_dependency, db: db_dependency, routine_request: RoutineCreate):
    db_routine = Routine(name=routine_request.name, description=routine_request.description, user_id=user.get("id"))
    for workout_id in routine_request.workouts:
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
        db_routine.workouts.append(workout)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    db_routines = db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id == db_routine.user_id).all()
    return db_routines

@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_routine(user: user_dependency, db: db_dependency, routine_id: int):
    db_routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if db_routine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
    db.delete(db_routine)
    db.commit()
    return db_routine

