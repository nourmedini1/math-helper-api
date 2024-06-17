from pydantic import BaseModel
from typing import Optional,List

class MatrixResponse(BaseModel) :
    matrix : Optional[str]
    eignValue : Optional[str]
    eignVector : Optional[str]
    determinant : Optional[str]
    rank : Optional[str]
    