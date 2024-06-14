from pydantic import BaseModel


class IntegralResponse(BaseModel) :
    integral : str 
    result : str 