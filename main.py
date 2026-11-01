from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, field_validator

app = FastAPI(title="Todo API")

lists_db: dict[int,dict] = {}
todos_db: dict[int, dict] = {}
list_id = 0
todo_id = 0

class ListCreate(BaseModel):
    title: str
    description: str | None = None

class ListRead(BaseModel):
    id: int
    title: str
    description: str | None = None

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    tags: list[str] = []

    @field_validator("tags", mode="before")
    def check(cls, v):
        if not v:
            return []
        return list(dict.fromkeys(tag.lower() for tag in v))

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    list_id: int

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    tags: list[str] | None = None

    @field_validator("tags", mode="before")
    def check(cls, v):
        if not v:
            return None
        return list(dict.fromkeys(tag.lower() for tag in v))
    






