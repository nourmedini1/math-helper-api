from pydantic import BaseModel
from typing import Union

class IntegralLimits(BaseModel):
    lowerLimit : Union[str,float,int]
    upperLimit : Union[str,float,int]