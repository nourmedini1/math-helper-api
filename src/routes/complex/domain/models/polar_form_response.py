from pydantic import BaseModel 

class PolarFormResponse(BaseModel) :
    algebraicForm : str 
    polarForm : str