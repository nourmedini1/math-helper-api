from pydantic import BaseModel
from typing import Union

class TaylorSeriesRequest(BaseModel):
    expression : str 
    near : Union[str,float,int] = 0
    order : int = 1
    variable : str