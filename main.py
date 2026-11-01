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
    done: bool = False

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
    
def get_list_or_404(list_id: int):
    if list_id not in lists_db:
        raise HTTPException(status_code=404, detail="List not found")
    return lists_db[list_id]

def get_todo_or_404(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]

@app.post("/lists", response_model=ListRead, status_code=201)
def create(list_data: ListCreate):
    global list_id
    list_id += 1
    new_list = {"id": list_id, **list_data.model_dump()}
    lists_db[list_id] = new_list
    return new_list

@app.get("/lists", response_model=list[ListRead])
def get_lists():
    return list(lists_db.values())

@app.get("/lists/{list_id}", response_model=ListRead)
def get_list(list_id: int):
    return get_list_or_404(list_id)

@app.delete("/lists/{list_id}", status_code=204)
def delete_list(list_id: int):
    get_list_or_404(list_id)
    del lists_db[list_id]

@app.post("/lists/{list_id}/todos", response_model=TodoRead, status_code=201)
def create_todo(list_id: int, todo_data: TodoCreate):
    get_list_or_404(list_id)
    global todo_id
    todo_id += 1
    new_todo = {"id": todo_id, "list_id": list_id, **todo_data.model_dump()}
    todos_db[todo_id] = new_todo
    return new_todo

@app.get("/lists/{list_id}/todos", response_model=list[TodoRead])
def get_todos(list_id: int, done: bool | None = None, tag: str | None = None):
    get_list_or_404(list_id)
    todos = [t for t in todos_db.values() if t["list_id"] == list_id]

    if done is not None:
        todos = [t for t in todos if t["done"] == done]

    if tag is not None:
        todos = [t for t in todos if tag.lower() in t["tags"]]

    return todos

@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int):
    return get_todo_or_404(todo_id)

@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, todo_data: TodoUpdate):
    todo = get_todo_or_404(todo_id)
    update_data = todo_data.model_dump(exclude_unset=True)
    todo.update(update_data)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    get_todo_or_404(todo_id)
    del todos_db[todo_id]