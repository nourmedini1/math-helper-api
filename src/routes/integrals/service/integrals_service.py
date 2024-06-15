import sympy as smp
from typing import Union,List
from routes.integrals.domain.models.integral_request import IntegralRequest
from routes.integrals.domain.models.integral_response import IntegralResponse
from utils.parse_input import InputParser
from routes.integrals.domain.models.integral_limits import IntegralLimits
import traceback

class IntegralsServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(IntegralsServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class IntegralsService(metaclass= IntegralsServiceMeta) :

    def _sympifyParameters(self,request : IntegralRequest) -> tuple[Union[str,List[smp.Symbol]]] : 
        sympifiedVariables = [smp.Symbol(variable) for variable in request.variables]
        sympifiedExpression = smp.simplify(smp.sympify(InputParser.parse_expression(request.expression)))
        return sympifiedExpression,sympifiedVariables
    
    def _latexifyResult(self,integral : str , result : str, indefinite : bool = True) -> tuple[str] :
        if indefinite :
            return smp.latex(integral),smp.latex(result) + " + c"
        else :
            return smp.latex(integral),smp.latex(result)
        
    def _setupIntegralLimits(self,limits : List[IntegralLimits]) -> List[IntegralLimits]:
        for integralLimits in limits :
            if isinstance(integralLimits.upperLimit,str) :
                integralLimits.upperLimit = InputParser.parse_expression(integralLimits.upperLimit)
            if isinstance(integralLimits.lowerLimit,str) :
                integralLimits.lowerLimit = InputParser.parse_expression(integralLimits.lowerLimit)
        return limits





    def singleIntegral(self,request : IntegralRequest) -> IntegralResponse :
        expression,variables = self._sympifyParameters(request)
        integral = smp.Integral(expression, variables[0])
        result = smp.integrate(expression,variables[0])
        latexifiedIntegral,latexifiedResult = self._latexifyResult(integral,result)
        return IntegralResponse(
            integral = latexifiedIntegral,
            result = latexifiedResult
        )
    
    def doubleIntegral(self,request : IntegralRequest) -> IntegralResponse :
        expression,variables = self._sympifyParameters(request)
        integral = smp.Integral(smp.Integral(expression, variables[0]),variables[1])
        result = smp.integrate(expression, variables[0] ,variables[1])
        latexifiedIntegral,latexifiedResult = self._latexifyResult(integral,result)
        return IntegralResponse(
            integral = latexifiedIntegral,
            result = latexifiedResult
        )
    
    def tripleIntegral(self,request : IntegralRequest) -> IntegralResponse :
        expression,variables = self._sympifyParameters(request)
        integral = smp.Integral(smp.Integral(smp.Integral(expression, variables[0]),variables[1]),variables[2])
        result = smp.integrate(expression, variables[0] ,variables[1],variables[2])
        latexifiedIntegral,latexifiedResult = self._latexifyResult(integral,result)
        return IntegralResponse(
            integral = latexifiedIntegral,
            result = latexifiedResult
        )
    
    def definiteSingleIntegral(self,request : IntegralRequest) -> IntegralResponse :
        try:
            expression,variables = self._sympifyParameters(request)
            limits = self._setupIntegralLimits(request.limits)
            integral = smp.Integral(expression, (variables[0],limits[0].lowerLimit,limits[0].upperLimit))
            result = smp.integrate(expression, (variables[0],limits[0].lowerLimit,limits[0].upperLimit))
            latexifiedIntegral,latexifiedResult = self._latexifyResult(integral,result,False)
            return IntegralResponse(
                integral = latexifiedIntegral,
                result = latexifiedResult
            )
        except Exception as e :
            traceback.print_exc()
            raise e

    def definiteDoubleIntegral(self,request : IntegralRequest) -> IntegralResponse :
        expression,variables = self._sympifyParameters(request)
        limits : List[IntegralLimits] = self._setupIntegralLimits(request.limits)
        integral = smp.Integral(
            smp.Integral(
                expression, 
                (variables[0],limits[0].lowerLimit,limits[0].upperLimit)),
                (variables[1],limits[1].lowerLimit,limits[1].upperLimit)
            )
        result = smp.integrate(
            expression, 
            (variables[0],limits[0].lowerLimit,limits[0].upperLimit),
            (variables[1],limits[1].lowerLimit,limits[1].upperLimit)
        )
        latexifiedIntegral,latexifiedResult = self._latexifyResult(integral,result,False)
        return IntegralResponse(
            integral = latexifiedIntegral,
            result = latexifiedResult
        )
    
    def definiteTripleIntegral(self,request : IntegralRequest) -> IntegralResponse :
        expression,variables = self._sympifyParameters(request)
        limits : List[IntegralLimits] = self._setupIntegralLimits(request.limits)
        integral = smp.Integral(
            smp.Integral(
                smp.Integral(
                    expression, 
                    (variables[0],limits[0].lowerLimit,limits[0].upperLimit)),
                    (variables[1],limits[1].lowerLimit,limits[1].upperLimit)),
                    (variables[2],limits[2].lowerLimit,limits[2].upperLimit)
        )
        result = smp.integrate(
            expression, 
            (variables[0],limits[0].lowerLimit,limits[0].upperLimit),
            (variables[1],limits[1].lowerLimit,limits[1].upperLimit),
            (variables[2],limits[2].lowerLimit,limits[2].upperLimit)
        )
        latexifiedIntegral,latexifiedResult = self._latexifyResult(integral,result,False)
        return IntegralResponse(
            integral = latexifiedIntegral,
            result = latexifiedResult
        )
    

        
