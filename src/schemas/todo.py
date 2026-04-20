from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=255)
    is_completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    is_completed: bool


class TodoGet(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Pagination(BaseModel):
    current_page: int
    total_pages: int
    total_records: int
    record_per_page: int
    previous_page_url: Optional[str]
    next_page_url: Optional[str]


class TodoListResponse(BaseModel):
    pagination: Pagination
    todos: List[TodoGet]
