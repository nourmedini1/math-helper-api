from pydantic import BaseModel
from typing import List

class DifferentialEquationResponse(BaseModel):
    equation : str 
    initialConditions : List[List[str]] = [["",""]]
    solution : str
    