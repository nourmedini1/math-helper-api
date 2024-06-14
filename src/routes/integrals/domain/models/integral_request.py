from typing import List,Optional
from pydantic import BaseModel
from routes.integrals.domain.models.integral_limits import IntegralLimits

class IntegralRequest(BaseModel):
    expression : str 
    variables : List[str]
    limits : Optional[List[IntegralLimits]]