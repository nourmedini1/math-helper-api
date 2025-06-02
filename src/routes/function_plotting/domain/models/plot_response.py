from pydantic import BaseModel
from typing import List, Union, Optional

class VariationTable(BaseModel):
    intervals: List[List[Union[float,str]]] = []
    values: List[List[Union[float, str]]] = []
    directions: List[str] = []
    firstDerivativeSign: List[str] = []
    secondDerivativeSign: List[str] = []

class PlotResponse(BaseModel):
    data: str
    pointsCount: int
    criticalPoints: List[List[float]] = []
    inflectionPoints: List[List[float]] = []
    variationTable: Optional[VariationTable] = None
    isFirstPlot: bool = True