from pydantic import BaseModel
from typing import Union

class DerivativeResponse(BaseModel):
    derivative : str 
    result : Union[str,float]
    
 
