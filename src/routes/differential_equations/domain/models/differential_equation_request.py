from pydantic import BaseModel 
from typing import List,Optional
from routes.differential_equations.domain.models.initial_condition import InitialCondition


class DifferentialEquationRequest(BaseModel):
    variable : str
    coefficients : List[Optional[str]]
    initialConditions : List[Optional[InitialCondition]]
    constant : Optional[str]
    rightHandSide : str = "0"

   