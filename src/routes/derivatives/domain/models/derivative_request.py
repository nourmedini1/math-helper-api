from pydantic import BaseModel
from typing import Optional


class DerivativeRequest(BaseModel):
    expression : str
    variable : str 
    order : int = 1 
    partial : bool = False
    derivingPoint : Optional[str]
    

