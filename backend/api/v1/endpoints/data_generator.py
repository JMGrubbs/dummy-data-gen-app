from datetime import datetime
from typing import Any

from fastapi import APIRouter, status
from services.reciver import send_data_to_reciver

router = APIRouter()


@router.post(path="/create", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def data_generator() -> dict[str, str]:
    package: dict[Any, Any] = {
        "number_of_requests": 5,
        "requests_per_min": 60,
        "data": {"name": "John Doe", "age": 30, "email": "JohnDoe@gmail.com", "timestamp": datetime.now()},
    }
    await send_data_to_reciver(data=package)

    return {"status": "ok"}
