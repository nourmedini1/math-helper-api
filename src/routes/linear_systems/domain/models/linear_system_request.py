from pydantic import BaseModel
from typing import List

class LinearSystemRequest(BaseModel):
    equations : List[str]
    variables : List[str]
    righHandSide : List[str]
