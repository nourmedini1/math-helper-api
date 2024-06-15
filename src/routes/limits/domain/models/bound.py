from pydantic import BaseModel
from typing import Union
class Bound(BaseModel):
    value : Union[str,float,int]
    sign : str = "+"