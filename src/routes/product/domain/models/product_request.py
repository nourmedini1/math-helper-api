from pydantic import BaseModel
from typing import Optional,Union

class ProductRequest(BaseModel):
    expression :str
    variable : str 
    lowerLimit : Optional[Union[str,int,float]]
    upperLimit : Optional[Union[str,int,float]]
