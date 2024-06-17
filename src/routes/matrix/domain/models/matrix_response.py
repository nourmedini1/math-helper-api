from pydantic import BaseModel
from typing import Optional

class MatrixResponse(BaseModel) :
    matrix : Optional[str]
    eigenValue : Optional[str]
    eigenVector : Optional[str]
    determinant : Optional[str]
    rank : Optional[str]
    