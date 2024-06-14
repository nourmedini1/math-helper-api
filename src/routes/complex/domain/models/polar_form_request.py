from pydantic import BaseModel
from typing import Union

class PolarFormRequest(BaseModel):
    real : Union[float,int]
    imaginary : Union[float,int]