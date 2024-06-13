from pydantic import BaseModel
from typing import Any

class ComplexOperationResponse(BaseModel) :
    z1 : str
    z2 : str
    polarZ1 : str
    polarZ2 : str
    algebraicResult : Any
    polarResult : Any