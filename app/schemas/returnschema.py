from pydantic import BaseModel

from typing import Optional, Any

class ReturnForm(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = None