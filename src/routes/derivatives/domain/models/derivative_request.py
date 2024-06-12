from pydantic import BaseModel
from enum import Enum
from typing import Optional

class DerivativeMethod(str, Enum):
    SYMBOLIC = "SYMBOLIC"
    NUMERIC = "NUMERIC"

class DerivativeRequest(BaseModel):
    method : DerivativeMethod = DerivativeMethod.SYMBOLIC
    expression : str
    variable : str 
    order : int = 1 
    partial : bool = False
    derivingPoint : Optional[str]
    

