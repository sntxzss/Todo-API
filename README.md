# Todo API

A FastAPI-based Todo management API that allows you to organize tasks into lists and manage individual todos.

## Getting Started

### Prerequisites
- Python 3.10+
- FastAPI
- Uvicorn

### Installation

```bash
pip install fastapi uvicorn pydantic
```

### Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## API Endpoints

### Lists

#### Create a List
- **POST** `/lists`
- Request body:
  ```json
  {
    "title": "Shopping",
    "description": "Items to buy"
  }
  ```
- Response: `201 Created`

#### Get All Lists
- **GET** `/lists`
- Response: Array of list objects

#### Get a Specific List
- **GET** `/lists/{list_id}`
- Response: Single list object or `404 Not Found`

#### Delete a List
- **DELETE** `/lists/{list_id}`
- Response: `204 No Content` or `404 Not Found`

### Todos in Lists

#### Create a Todo
- **POST** `/lists/{list_id}/todos`
- Request body:
  ```json
  {
    "title": "Buy milk",
    "description": "2% milk",
    "tags": ["grocery", "dairy"],
    "done": false
  }
  ```
- Response: `201 Created` or `404 Not Found` (if list doesn't exist)

#### Get Todos from a List
- **GET** `/lists/{list_id}/todos`
- Query parameters:
  - `done` (boolean, optional): Filter by completion status
  - `tag` (string, optional): Filter by tag (case-insensitive)
- Examples:
  - `/lists/1/todos` - All todos in list 1
  - `/lists/1/todos?done=true` - Completed todos only
  - `/lists/1/todos?tag=grocery` - Todos tagged with "grocery"
  - `/lists/1/todos?done=false&tag=work` - Incomplete work-related todos
- Response: Array of todo objects or `404 Not Found` (if list doesn't exist)

### Individual Todos

#### Get a Todo
- **GET** `/todos/{todo_id}`
- Response: Single todo object or `404 Not Found`

#### Update a Todo
- **PATCH** `/todos/{todo_id}`
- Request body (all fields optional):
  ```json
  {
    "title": "Buy 2% milk",
    "description": "Cold milk",
    "tags": ["grocery"],
    "done": true
  }
  ```
- Response: Updated todo object or `404 Not Found`

#### Delete a Todo
- **DELETE** `/todos/{todo_id}`
- Response: `204 No Content` or `404 Not Found`

## Data Models

### List
```json
{
  "id": 1,
  "title": "Shopping",
  "description": "Items to buy"
}
```

### Todo
```json
{
  "id": 1,
  "list_id": 1,
  "title": "Buy milk",
  "description": "2% milk",
  "tags": ["grocery", "dairy"],
  "done": false
}
```

## Features

- **Tag Management**: Automatically deduplicates and lowercases tags
- **Flexible Filtering**: Filter todos by completion status and tags
- **Partial Updates**: Update only the fields you need with PATCH
- **RESTful Design**: Standard HTTP methods and status codes

## Error Handling

- **404 Not Found**: Returned when a resource doesn't exist
- **400 Bad Request**: Returned for invalid request data
- **204 No Content**: Returned for successful deletions
