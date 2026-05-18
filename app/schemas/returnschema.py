from pydantic import BaseModel

from typing import Optional, Any

class ReturnForm(BaseModel): #Универсальный
    success: bool
    message: str
    error_code: Optional[str] = None
    data: Optional[Any] = None
    total: Optional[int] = None
    page: Optional[int] = None
    total_pages: Optional[int] = None
    limit: Optional[int] = None
    id: Optional[int] = None