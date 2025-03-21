from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Request, Depends

from config.logger import logger
from config.database import get_db
from utils.helper import ResponseHelper

from models.auth import ApiKey

router = APIRouter()
response = ResponseHelper()


## This is an example API endpoint. Make sure to remove this when you start building your own APIs
@router.get("/apikey")
async def get_apikey(
    request: Request,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Base query with filtering logic
    query = db.query(ApiKey).filter(
        ApiKey.is_deleted == False)

    # Calculate pagination
    total_records = query.count()
    total_pages = (total_records + limit - 1) // limit
    offset = (page - 1) * limit

    # Fetch paginated data
    data_list = (
        query.order_by(ApiKey.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Format data
    formatted_data = [
        {
            "id": api_key.id,
            "key": api_key.key,
            "is_active": api_key.is_active,
            "created_at": api_key.created_at,
        }
        for api_key in data_list
    ]

    # Generate pagination URLs
    base_url = str(request.url.path)
    previous_page_url = f"{base_url}?page={page - 1}&limit={limit}" if page > 1 else None
    next_page_url = f"{base_url}?page={page + 1}&limit={limit}" if page < total_pages else None

    # Prepare the final response
    resp_data = {
        "data": {
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_records": total_records,
                "previous_page_url": previous_page_url,
                "next_page_url": next_page_url,
                "record_per_page": limit,
            },
            "api_keys": formatted_data,
        }
    }

    return response.success_response(200, "success", data=resp_data)
