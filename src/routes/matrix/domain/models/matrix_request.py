from pydantic import BaseModel
from typing import List,Optional

class MatrixRequest(BaseModel):
    matrixA : List[List[float]]
    matrixB : Optional[List[List[float]]]


