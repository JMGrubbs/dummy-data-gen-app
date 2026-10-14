from pydantic import BaseModel


class DataGeneratorResponse(BaseModel):
    status: str
