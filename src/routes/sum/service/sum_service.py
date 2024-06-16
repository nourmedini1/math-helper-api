import traceback
import sympy as smp
from typing import Union
from routes.sum.domain.models.sum_request import SumRequest
from routes.sum.domain.models.sum_response import SumResponse
from utils.parse_input import InputParser

class SumServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SumServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class SumService(metaclass= SumServiceMeta) :

    def _setupLimits(self,lowerLimit : Union[str,int,float], upperLimit : Union[str,int,float]) :
        if lowerLimit == "-oo" : 
            lowerLimit = -smp.oo
        if upperLimit == "oo" :
            upperLimit = smp.oo
        return lowerLimit,upperLimit

    def _setupParameters(self,request : SumRequest) -> tuple[str] :
        variable = smp.Symbol(request.variable)
        expression = smp.sympify(InputParser.parse_expression(request.expression))
        lowerLimit,upperLimit = self._setupLimits(request.lowerLimit,request.upperLimit)
        return expression,variable,lowerLimit,upperLimit
    
    def symbolicSum(self, request : SumRequest) -> SumResponse :  
        try :      
            expression,variable,lowerLimit,upperLimit = self._setupParameters(request)
            summation = smp.Sum(expression,(variable,lowerLimit,upperLimit))  
            if summation.is_convergent() :
                convergent = True
                try :
                    result = smp.simplify(smp.summation(expression,(variable,lowerLimit,upperLimit)))
                except Exception:
                    result = "no symbolic form found"
            else :
                convergent = False
                result = ""
            return SumResponse(
                convergent= convergent,
                summation = smp.latex(summation),
                result = smp.latex(result)
                )
        except Exception as e:
            traceback.print_exc()
            raise e

        
    def numericSum(self,request : SumRequest) -> SumResponse :
        expression,variable,lowerLimit,upperLimit = self._setupParameters(request)
        summation = smp.Sum(expression,(variable,lowerLimit,upperLimit))
        if summation.is_convergent() :
            convergent = True
            try :
                result = smp.N(smp.Sum(expression,(variable,lowerLimit,upperLimit)))
            except Exception:
                result = "no numeric form found"
        else :
            convergent = False
            result = ""
        return SumResponse(
            convergent= convergent,
            summation = smp.latex(summation),
            result = smp.latex(result)
            )

        