import sympy as smp
from ....utils.parse_input import InputParser
from typing import Union
from ..domain.models.derivative_request import DerivativeRequest
from ..domain.models.derivative_response import DerivativeResponse
import traceback

class DerivativesServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DerivativesServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
   

class DerivativesService(metaclass=DerivativesServiceMeta) : 

    def _sympifyExpressions(self, variable : str, expression : str) -> tuple[str] :
        x = smp.Symbol(variable)
        f = smp.sympify(smp.simplify(expression))
        return x, f
    
    def _parseDerivingPoint(self, derivingPoint : str) -> Union[str,float] :
        if derivingPoint.isnumeric() :
            return float(derivingPoint)
        return derivingPoint
    
    def _latexifyDerivativeExpression(self, variable : str , order : int, isPartialDerivative : bool) -> str : 
        if isPartialDerivative : 
            if order > 1 :
                return "\\frac{\partial^" + str(order) + "f}{\partial^" + str(order) + smp.latex(variable) + "} = "
            else:
                return "\\frac{\partial f}{\partial " + smp.latex(variable) + "} = "
        else:
            if order > 1:
                return "\\frac{\mathrm{d}^" + str(order) + "f}{\mathrm{d}^" + str(order) + smp.latex(variable) + " } = "
            else:
                return "\\frac{\mathrm{d}f}{\mathrm{d}" + smp.latex(variable) + " } = "   
                        
    def symbolicDerivative(self, derivativeRequest : DerivativeRequest) -> DerivativeResponse : 
        try :
            variable,expression = self._sympifyExpressions(
                variable= derivativeRequest.variable,
                expression= InputParser.parse_expression(derivativeRequest.expression)
            )
            latexifiedExpression = self._latexifyDerivativeExpression(
                variable=variable, 
                order= derivativeRequest.order, 
                isPartialDerivative= derivativeRequest.partial
            )
            result = smp.latex(smp.diff(expression,variable,derivativeRequest.order))
            return DerivativeResponse(
                derivative= latexifiedExpression, 
                result= result
            )
        except Exception as e : 
            traceback.print_exc()
            raise e
        
    def numericDerivative(self, derivativeRequest : DerivativeRequest) -> DerivativeResponse :
        try : 
            variable,expression = self._sympifyExpressions(
                variable= derivativeRequest.variable,
                expression= InputParser.parse_expression(derivativeRequest.expression)
            )
            derivingPoint = self._parseDerivingPoint(derivativeRequest.derivingPoint)
            latexifiedExpression = self._latexifyDerivativeExpression(
                variable=variable, 
                order= derivativeRequest.order, 
                isPartialDerivative= derivativeRequest.partial
            )
            result = smp.latex(smp.diff(expression,variable,derivativeRequest.order).subs(variable,derivingPoint))
            return DerivativeResponse(
                derivative= latexifiedExpression, 
                result= result
            )
        except Exception as e : 
            traceback.print_exc()
            raise e
            





