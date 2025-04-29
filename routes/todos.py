from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends

from config.logger import logger
from config.database import get_db
from utils.auth import get_api_key
from utils.helper import ResponseHelper

from models.todo import Todo
from schemas.todo import TodoCreate, TodoUpdate, TodoGet, Pagination, TodoListResponse

router = APIRouter(prefix="/todos", tags=["Todos"])
response = ResponseHelper()


@router.get("")
async def get_todos(
    request: Request,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    query = Todo.get_active(db)

    total_records = query.count()
    total_pages = (total_records + limit - 1) // limit
    offset = (page - 1) * limit

    data_list = (
        query.order_by(Todo.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    todos = [TodoGet.model_validate(todo) for todo in data_list]

    base_url = str(request.url.path)
    previous_page_url = f"{base_url}?page={page - 1}&limit={limit}" if page > 1 else None
    next_page_url = f"{base_url}?page={page + 1}&limit={limit}" if page < total_pages else None

    pagination_data = Pagination(
        current_page=page,
        total_pages=total_pages,
        total_records=total_records,
        record_per_page=limit,
        previous_page_url=previous_page_url,
        next_page_url=next_page_url
    )
    resp_data = TodoListResponse(
        todos=todos,
        pagination=pagination_data
    )

    return response.success_response(200, "success", data=resp_data)


@router.get("/{todo_id}")
async def get_todo(
    todo_id: int,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    todo = Todo.get_active(db).filter(Todo.id == todo_id).first()

    if not todo:
        return response.error_response(404, "Todo not found")

    resp_data = TodoGet.model_validate(todo)

    return response.success_response(200, "success", data=resp_data)


@router.post("")
async def create_todo(
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

    resp_data = TodoGet.model_validate(new_todo)

    return response.success_response(201, "Todo created successfully", data=resp_data)


@router.put("/{todo_id}")
async def update_todo(
    todo_id: int,
    request: Request,
    data: TodoUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    todo = Todo.get_active(db).filter(Todo.id == todo_id).first()

    if not todo:
        return response.error_response(404, "Todo not found")

    todo.title = data.title
    todo.description = data.description
    todo.is_completed = data.is_completed

    todo.updated_at = datetime.now()

    db.commit()
    db.refresh(todo)

    resp_data = TodoGet.model_validate(todo)

    return response.success_response(200, "Todo updated successfully", data=resp_data)


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(get_api_key)
):
    todo = Todo.get_active(db).filter(Todo.id == todo_id).first()

    if not todo:
        return response.error_response(404, "Todo not found")

    todo.soft_delete()
    db.commit()

    return response.success_response(200, "Todo deleted successfully")
