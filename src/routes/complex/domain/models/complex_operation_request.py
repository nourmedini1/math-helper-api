from pydantic import BaseModel
from typing import Union






class ComplexOperationRequest(BaseModel):
    real1 : Union[float,int]
    imaginary1 : Union[float,int]
    real2 : Union[float,int]
    imaginary2 : Union[float,int]
   

    