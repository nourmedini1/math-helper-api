from routes.taylor_series.domain.models.taylor_series_request import TaylorSeriesRequest
from routes.taylor_series.domain.models.taylor_series_response import TaylorSeriesResponse
import sympy as smp
from utils.parse_input import InputParser
from typing import Any



class TaylorSeriesServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(TaylorSeriesServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class TaylorSeriesService(metaclass= TaylorSeriesServiceMeta) :

    def _sympifyParameters(self,request : TaylorSeriesRequest) -> tuple[Any] :
        sympifiedVariable = smp.Symbol(request.variable)
        sympifiedExpression = smp.simplify(smp.sympify(InputParser.parse_expression(request.expression)))
        if isinstance(request.near,str) :
            request.near = smp.sympify(request.near)
        return sympifiedExpression,sympifiedVariable,request.near
    
    
    def taylorSeries(self,request : TaylorSeriesRequest) -> TaylorSeriesResponse :
        expression,variable,near = self._sympifyParameters(request)
        series = smp.series(smp.simplify(expression),variable,near,n=request.order)
        return TaylorSeriesResponse(
            expression = smp.latex(expression),
            result = smp.latex(series)
        )