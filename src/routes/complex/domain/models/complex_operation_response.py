from pydantic import BaseModel

class ComplexOperationResponse(BaseModel) :
    z1 : str
    z2 : str
    polarZ1 : str
    polarZ2 : str
    algebraicResult : str
    polarResult : str