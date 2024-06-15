from pydantic import BaseModel
from typing import List
from routes.limits.domain.models.bound import Bound

class LimitRequest(BaseModel):
    expression : str
    variables : List[str]
    bounds : List[Bound]