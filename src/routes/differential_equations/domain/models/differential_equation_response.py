from pydantic import BaseModel
from typing import List

class DifferentialEquationResponse(BaseModel):
    equation : str 
    solution : str
    