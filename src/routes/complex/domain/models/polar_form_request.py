from pydantic import BaseModel

class PolarFormRequest(BaseModel):
    real : float
    imaginary : float 