from pydantic import BaseModel

class PlotRequest(BaseModel):
    function: str
    precision: int
    lower_bound: float = None
    upper_bound: float = None
    max_points: int = 3000