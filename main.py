from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
import models
from database import engine, session_local
import uvicorn


app = FastAPI()

models.base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()


class Tuple(BaseModel):
    name: str = Field(min_length=1)
    todo: str = Field(min_length=1)


@app.get("/")
def get_api():
    return {"message": "working"}

@app.post("/user")
def create_Tuple(Tuple: Tuple):
    Tuple_model = models.Tuples()
    Tuple_model.name = Tuple.name
    Tuple_model.todo = Tuple.todo

    db = session_local()
    db.add(Tuple_model)
    db.commit()

    return Tuple

@app.get("/todo")
def get_todo():
    db = session_local()
    res = db.query(models.Tuples).all()
    db.close()
    return res

@app.put("/todo/{user_id}")
def edit_Tuple(user_id: int, Tuple: Tuple):
    db = session_local()

    user = db.query(models.Tuples).filter(models.Tuples.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})

    user.todo = Tuple.todo
    db.commit()

    db.close()
    return {"message": "Change is complete"}

@app.delete("/user/{user_id}")
def delete_Tuple(user_id: int):
    db = session_local()

    user = db.query(models.Tuples).filter(models.Tuples.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})

    db.delete(user)
    db.commit()

    db.close()
    return {"message": "The user has been successfully deleted"}