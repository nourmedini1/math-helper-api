from pydantic import BaseModel
from typing import List,Union

class LinearSystemRequest(BaseModel):
    equations : List[str]
    variables : List[str]
    righHandSide : List[Union[str,float,int]]
