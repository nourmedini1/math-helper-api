from pydantic import BaseModel
from typing import Optional

class MatrixResponse(BaseModel) :
    matrixA : Optional[str] = None
    matrixB : Optional[str] = None
    matrix : Optional[str] = None
    eigenValue : Optional[str] = None
    eigenVector : Optional[str] = None
    determinant : Optional[str] = None
    rank : Optional[str] = None
    