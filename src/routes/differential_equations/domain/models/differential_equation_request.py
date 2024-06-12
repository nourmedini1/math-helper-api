from pydantic import BaseModel 
from typing import List,Optional


class DifferentialEquationRequest(BaseModel):
    variable : str
    firstCoefficient : Optional[str]
    secondCoefficient : Optional[str]
    thirdCoefficient : Optional[str]
    firstInitialCondition = Optional[List[str]]
    secondInitialCondition = Optional[List[str]] 
    thirdInitialCondition = Optional[List[str]] 
    constant : Optional[str]
    rightHandSide : str = "0"

   