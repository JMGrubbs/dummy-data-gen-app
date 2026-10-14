from datetime import datetime
from typing import Any

from pydantic import BaseModel

default_package: dict[str, Any] = {
    "number_of_requests": 5,
    "requests_per_min": 60,
    "data": {"name": "John Doe", "age": 30, "email": "JohnDoe@gmail.com", "timestamp": datetime.now().timestamp()},
}
url_destination: str = "http://reciver:8000"


class DataGeneratorResponse(BaseModel):
    status: str


class PackageFormat(BaseModel):
    number_of_requests: int
    requests_per_min: int
    data: dict[str, Any]
    url_destination: str = url_destination
