from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Request, Depends

from config.logger import logger
from config.database import get_db
from utils.auth import get_api_key
from utils.helper import ResponseHelper

from models.todo import Todo

router = APIRouter()
response = ResponseHelper()


@router.get("/todos")
async def get_todos(
    request: Request,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    # Base query with filtering logic
    query = db.query(Todo).filter(
        Todo.is_deleted == False)

    # Calculate pagination
    total_records = query.count()
    total_pages = (total_records + limit - 1) // limit
    offset = (page - 1) * limit

    # Fetch paginated data
    data_list = (
        query.order_by(Todo.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Format data
    formatted_data = [
        {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "is_completed": todo.is_completed,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at,
        }
        for todo in data_list
    ]

    # Generate pagination URLs
    base_url = str(request.url.path)
    previous_page_url = f"{base_url}?page={page - 1}&limit={limit}" if page > 1 else None
    next_page_url = f"{base_url}?page={page + 1}&limit={limit}" if page < total_pages else None

    # Prepare the final response
    resp_data = {
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_records": total_records,
            "record_per_page": limit,
            "previous_page_url": previous_page_url,
            "next_page_url": next_page_url,
        },
        "todos": formatted_data,
    }

    return response.success_response(200, "success", data=resp_data)


@router.get("/todos/{todo_id}")
async def get_todo(
    todo_id: int,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    todo = db.query(Todo).filter(Todo.id == todo_id,
                                 Todo.is_deleted == False).first()

    if not todo:
        return response.error_response(404, "Todo not found")

    resp_data = {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "is_completed": todo.is_completed,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at,
    }

    return response.success_response(200, "success", data=resp_data)


class TodoCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=255)
    is_completed: bool = Field(False)


@router.post("/todos")
def create_todo(
    data: TodoCreate,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    new_todo = Todo(
        title=data.title,
        description=data.description,
        is_completed=data.is_completed
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    resp_data = {
        "id": new_todo.id,
        "title": new_todo.title,
        "description": new_todo.description,
        "is_completed": new_todo.is_completed,
        "created_at": new_todo.created_at,
        "updated_at": new_todo.updated_at,
    }

    return response.success_response(201, "Todo created successfully", data=resp_data)


class TodoUpdate(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=255)
    is_completed: bool


@router.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    request: Request,
    data: TodoUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    todo = db.query(Todo).filter(Todo.id == todo_id,
                                 Todo.is_deleted == False).first()

    if not todo:
        return response.error_response(404, "Todo not found")

    # Update fields if provided
    todo.title = data.title
    todo.description = data.description
    todo.is_completed = data.is_completed

    todo.updated_at = datetime.now()

    db.commit()
    db.refresh(todo)

    resp_data = {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "is_completed": todo.is_completed,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at,
    }

    return response.success_response(200, "Todo updated successfully", data=resp_data)


@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    todo = db.query(Todo).filter(Todo.id == todo_id,
                                 Todo.is_deleted == False).first()

    if not todo:
        return response.error_response(404, "Todo not found")

    # Soft delete
    todo.is_deleted = True
    db.commit()

    return response.success_response(200, "Todo deleted successfully")
