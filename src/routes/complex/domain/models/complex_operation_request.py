from pydantic import BaseModel
from enum import Enum

class ComplexOperation(Enum) :
    ADDITION = "ADDITION"
    SUBSTRACTION = "SUBSTRACTION"
    MULTIPLICATION = "MULTIPLICATION"



class ComplexOperationRequest(BaseModel):
    real1 : float
    imaginary1 : float
    real2 : float
    imaginary2 : float
   

    