from pydantic import BaseModel

class PlotResponse(BaseModel):
    data : str
    points_count : int
    critical_points : list[list[float]] = []
    inflection_points : list[list[float]] = []