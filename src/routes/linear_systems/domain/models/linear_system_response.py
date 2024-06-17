from typing import Optional
from pydantic import BaseModel



class LinearSystemResponse(BaseModel):
    linearSystem : str
    result : Optional[str]