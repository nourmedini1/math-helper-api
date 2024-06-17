from pydantic import BaseModel

class ProductResponse(BaseModel) :
    convergent : bool
    product : str 
    result : str
