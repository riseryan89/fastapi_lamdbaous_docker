from datetime import datetime
from pydantic import BaseModel

class GetCode(BaseModel):
    code: str


class CodeRunResult(BaseModel):
    statusCode: int = None
    body: str = None

    class Config:
        orm_mode = True
