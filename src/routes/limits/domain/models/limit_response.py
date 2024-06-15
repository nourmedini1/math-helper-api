from pydantic import BaseModel 

class LimitResponse(BaseModel):
    limit: str 
    result : str 