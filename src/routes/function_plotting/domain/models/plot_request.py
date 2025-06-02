from pydantic import BaseModel

class PlotRequest(BaseModel):
    function: str
    precision: int
    lowerBound: float = None
    upperBound: float = None
    maxPoints: int = 3000
    isFirstPlot : bool 