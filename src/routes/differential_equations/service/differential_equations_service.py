from typing import List,Optional,Dict
from ....utils.parse_input import InputParser
import sympy as smp
from ..domain.models.differential_equation_request import DifferentialEquationRequest
from ..domain.models.differential_equation_response import DifferentialEquationResponse 
import traceback

class DifferentialEquationsServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DifferentialEquationsServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DifferentialEquationsService(metaclass= DifferentialEquationsServiceMeta) :
    
    
    def _parseCoefficients(
            firstCoefficient : Optional[str], 
            secondCoefficient : Optional[str],
            thirdCoefficient : Optional[str],
            fourthCoefficient : Optional[str]
            ) -> List[str] :
        
        parsedCoefficients : List[str] = []

        if firstCoefficient is not None :
            parsedCoefficients.append(smp.sympify(InputParser.parse_expression(firstCoefficient)))

        if secondCoefficient is not None :
            parsedCoefficients.append(smp.sympify(InputParser.parse_expression(secondCoefficient)))

        if thirdCoefficient is not None :
            parsedCoefficients.append(smp.sympify(InputParser.parse_expression(thirdCoefficient)))
        
        if fourthCoefficient is not None :
            parsedCoefficients.append(smp.sympify(InputParser.parse_expression(fourthCoefficient)))

        return parsedCoefficients
    
    
    def _parseInitialConditions(
            firstInitialCondition : Optional[List[str]],
            secondInitialCondition : Optional[List[str]],
            thirdInitialCondition : Optional[List[str]],
            fourthInitialCondition : Optional[List[str]],
            f : smp.Function,
            variable : smp.Symbol
        ) -> Dict :

        ics = {}
        if firstInitialCondition not in [None,""] : 
            ics[f(firstInitialCondition[0])] = firstInitialCondition[1]

        if secondInitialCondition not in [None,""] :
            ics[f(variable).diff(variable).subs(variable,secondInitialCondition[0])] = secondInitialCondition[1]

        if thirdInitialCondition not in [None,""] :
            ics[f(variable).diff(variable,2).subs(variable,thirdInitialCondition[0])] = thirdInitialCondition[1]

        if fourthInitialCondition not in [None,""] :
            ics[f(variable).diff(variable,3).subs(variable,fourthInitialCondition[0])] = fourthInitialCondition[1]

        return ics
    
    def _setupEquationParameters(self,request : DifferentialEquationRequest) -> tuple[any] :
        variable = smp.Symbol(request.variable)
        f = smp.Function('f')
        constant = smp.sympify(InputParser.parse_expression(request.constant))
        rightHandSide = smp.sympify(InputParser.parse_expression(request.rightHandSide))
        coefficients = self._parseCoefficients(
            request.firstCoefficient,
            request.secondCoefficient,
            request.thirdCoefficient,
            request.fourthCoefficient)
        initialConditions = self._parseInitialConditions(
            request.firstInitialCondition,
            request.secondInitialCondition,
            request.thirdInitialCondition,
            request.fourthInitialCondition,
            f,
            variable)
        return variable,f,constant,rightHandSide,coefficients,initialConditions

    def latexifyResult(equation : str , solution : str) -> tuple[str] :
        return smp.latex(equation),smp.latex(solution)
    
    def firstOrderDifferentialEquation(self,request : DifferentialEquationRequest) -> DifferentialEquationResponse :
        try : 
            variable,f,constant,rightHandSide,coefficients,initialConditions = self._setupEquationParameters(request)    
            equation = smp.Eq(coefficients[0]*f(variable) + coefficients[1]*f(variable).diff(variable) + constant, rightHandSide)
            solution = smp.dsolve(equation, f, ics=initialConditions)
            latexifiedEquation,latexifiedSolution = self.latexifyResult(equation,solution)
            return DifferentialEquationResponse(solution=latexifiedSolution,equation=latexifiedEquation)
        except Exception as e : 
            traceback.print_exc()
            raise e
        
    def secondOrderDifferentialEquation(self,request : DifferentialEquationRequest) -> DifferentialEquationResponse :
        try :
            variable,f,constant,rightHandSide,coefficients,initialConditions = self._setupEquationParameters(request)    
            equation = smp.Eq(
                coefficients[2]*f(variable).diff(variable,2) 
                + coefficients[1]*f(variable).diff(variable) 
                + coefficients[0]*f(variable) 
                + constant, 
                rightHandSide)
            solution = smp.dsolve(equation, f, ics=initialConditions)
            latexifiedEquation,latexifiedSolution = self.latexifyResult(equation,solution)
            return DifferentialEquationResponse(solution=latexifiedSolution,equation=latexifiedEquation)
        except Exception as e :
            traceback.print_exc()
            raise e
        
    def thirdOrderDifferentialEquation(self,request : DifferentialEquationRequest) -> DifferentialEquationResponse :
        try :
            variable,f,constant,rightHandSide,coefficients,initialConditions = self._setupEquationParameters(request)
            equation = smp.Eq(
                coefficients[2]*f(variable).diff(variable,2) 
                + coefficients[1]*f(variable).diff(variable) 
                + coefficients[0]*f(variable) 
                + constant, 
                rightHandSide)
            solution = smp.dsolve(equation, f, ics=initialConditions)
            latexifiedEquation,latexifiedSolution = self.latexifyResult(equation,solution)
            return DifferentialEquationResponse(solution=latexifiedSolution,equation=latexifiedEquation)
        except Exception as e :
            traceback.print_exc()
            raise e

        
