from routes.limits.domain.models.limit_request import LimitRequest
from routes.limits.domain.models.limit_response import LimitResponse
from utils.parse_input import InputParser
from typing import Any,List
from routes.limits.domain.models.bound import Bound 
import sympy as smp

class LimitsServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(LimitsServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class LimitsService(metaclass= LimitsServiceMeta) :

    def _setupLimitBounds(bounds : List[Bound]) -> List[Bound] :
        for bound in bounds : 
            if isinstance(bound.value,str) :
                bound.value = smp.sympify(InputParser.parse_expression(bound.value))

    def _sympifyParameters(self,request : LimitRequest) -> tuple[Any] : 
        sympifiedVariables = [smp.Symbol(variable) for variable in request.variables]
        sympifiedExpression = smp.simplify(smp.sympify(InputParser.parse_expression(request.expression)))
        sympifiedBounds = self._setupLimitBounds(request.bounds)
        return sympifiedExpression,sympifiedVariables,sympifiedBounds
        

    def singleLimit(self,request : LimitRequest) -> LimitResponse :
        expression,variables,bounds = self._sympifyParameters(request)
        limit = smp.Limit(expression,variables[0],bounds[0].value,bounds[0].sign)
        result = limit.doit().evalf()
        return LimitResponse(
            limit = smp.latex(limit),
            result = smp.latex(result)
        )
    
    def doubleLimit(self,request : LimitRequest) -> LimitResponse :
        expression,variables,bounds = self._sympifyParameters(request)
        limit = smp.Limit(expression, tuple(variables), (bounds[0].value,bounds[1].value), bounds[0].sign)
        result = expression.limit(variables[0], bounds[0].value, bounds[0].sign).limit(variables[1], bounds[1].value,bounds[1].sign).evalf()
        return LimitResponse(
            limit = smp.latex(limit),
            result = smp.latex(result)
        )
    
    def tripleLimit(self,request : LimitRequest) -> LimitResponse :
        expression,variables,bounds = self._sympifyParameters(request)
        limit = smp.Limit(expression, tuple(variables), (bounds[0].value,bounds[1].value,bounds[2].value), bounds[0].sign)
        result = expression.limit(
            variables[0], bounds[0].value, bounds[0].sign).limit(
                variables[1], bounds[1].value,bounds[1].sign).limit(
                    variables[2], bounds[2].value,bounds[2].sign).evalf()
        return LimitResponse(
            limit = smp.latex(limit),
            result = smp.latex(result)
        )


