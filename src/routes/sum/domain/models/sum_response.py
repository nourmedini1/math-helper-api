from pydantic import BaseModel

class SumResponse(BaseModel) :
    convergent : bool
    summation : str 
    result : str
