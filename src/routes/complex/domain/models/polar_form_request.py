from pydantic import BaseModel


class PolarFormRequest(BaseModel):
    real : str
    imaginary : str