from pydantic import BaseModel
from typing import Union

class TaylorSeriesRequest(BaseModel):
    expression : str 
    near : Union[str,float,int]
    order : int
    variable : str