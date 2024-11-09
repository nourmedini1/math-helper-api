from pydantic import BaseModel







class ComplexOperationRequest(BaseModel):
    real1 : str
    imaginary1 : str
    real2 : str
    imaginary2 : str
   

    