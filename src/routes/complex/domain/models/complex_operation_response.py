from pydantic import BaseModel

class ComplexOperationResponse(BaseModel) :
    z1 : str
    z2 : str
    PolarZ1 : str
    PolarZ2 : str
    algebraicResult : str
    polarResult : str