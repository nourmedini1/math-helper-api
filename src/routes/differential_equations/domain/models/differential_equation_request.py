from pydantic import BaseModel 
from typing import List


class DifferentialEquationRequest(BaseModel):
    variable : str
    firstCoefficient : str = ""
    secondCoefficient : str = ""
    thirdCoefficient : str = ""
    firstInitialCondition = List[str] = ["",""]
    secondInitialCondition = List[str] = ["",""]
    thirdInitialCondition = List[str] = ["",""]
    constant : str = ""
    rightHandSide : str = ""

   