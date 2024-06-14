from pydantic import BaseModel

class InitialCondition(BaseModel):
    x : str = "" 
    y : str = ""