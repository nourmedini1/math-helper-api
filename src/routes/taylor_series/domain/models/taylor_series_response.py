from pydantic import BaseModel

class TaylorSeriesResponse(BaseModel):
    expression : str 
    result : str