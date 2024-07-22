from typing import List,Optional,Dict
from routes.differential_equations.domain.models.initial_condition import InitialCondition
from utils.parse_input import InputParser
import sympy as smp
from routes.differential_equations.domain.models.differential_equation_request import DifferentialEquationRequest
from routes.differential_equations.domain.models.differential_equation_response import DifferentialEquationResponse 
import traceback

class DifferentialEquationsServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DifferentialEquationsServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DifferentialEquationsService(metaclass= DifferentialEquationsServiceMeta) :
    
    
    def _parseCoefficients(
            self,
            coefficients : List[Optional[str]],
            ) -> List[str] :
        
        parsedCoefficients : List[str] = []
        for coefficient in coefficients :
            if coefficient is not None :
                parsedCoefficients.append(smp.sympify(InputParser.parse_expression(coefficient)))
            else :
                parsedCoefficients.append(smp.sympify("1"))
        return parsedCoefficients

    
    def _parseInitialConditions(
        self,
        initialConditions : List[Optional[InitialCondition]],
        f : smp.Function,
        variable : smp.Symbol) -> Dict :

        ics = {}
        for i,initialCondition in enumerate(initialConditions):
            if initialCondition is not None :
                if i == 0 : 
                    ics[f(initialCondition.x)] = initialCondition.y
                else :
                    ics[f(variable).diff(variable,i).subs(variable,initialCondition.x)] = initialCondition.y
        return ics
    
    def _setupEquationParameters(self,request : DifferentialEquationRequest) -> tuple[any] :
        variable = smp.Symbol(request.variable)
        f = smp.Function('f')
        constant = smp.sympify(InputParser.parse_expression(request.constant))
        rightHandSide = smp.sympify(InputParser.parse_expression(request.rightHandSide))
        coefficients = self._parseCoefficients(request.coefficients)
        initialConditions = self._parseInitialConditions(request.initialConditions,f,variable)
        return variable,f,constant,rightHandSide,coefficients,initialConditions

    def latexifyResult(self,equation : str , solution : str) -> tuple[str] :
        return smp.latex(equation),smp.latex(solution)
    
    def firstOrderDifferentialEquation(self,request : DifferentialEquationRequest) -> DifferentialEquationResponse :
        try : 
            variable,f,constant,rightHandSide,coefficients,initialConditions = self._setupEquationParameters(request)    
            equation = smp.Eq(coefficients[0]*f(variable) + coefficients[1]*f(variable).diff(variable) + constant, rightHandSide)
            solution = smp.dsolve(equation,ics=initialConditions).simplify()
            returnedEquation = smp.Eq(
                coefficients[1]*smp.Symbol("y'") 
                + coefficients[0]*smp.Symbol("y") 
                + constant, 
                rightHandSide)
            latexifiedEquation,latexifiedSolution = self.latexifyResult(returnedEquation,solution)
            return DifferentialEquationResponse(solution=latexifiedSolution.replace("f{\\left(x \\right)}","y"),equation=latexifiedEquation)
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
            solution = smp.dsolve(equation,ics=initialConditions).simplify()
            returnedEquation = smp.Eq(coefficients[2]*smp.Symbol("y''") 
                + coefficients[1]*smp.Symbol("y'") 
                + coefficients[0]*smp.Symbol("y") 
                + constant, 
                rightHandSide)
            latexifiedEquation,latexifiedSolution = self.latexifyResult(returnedEquation,solution)
            return DifferentialEquationResponse(solution=latexifiedSolution.replace("f{\\left(x \\right)}","y"),equation=latexifiedEquation)
        except Exception as e :
            traceback.print_exc()
            raise e
        
    def thirdOrderDifferentialEquation(self,request : DifferentialEquationRequest) -> DifferentialEquationResponse :
        try :
            variable,f,constant,rightHandSide,coefficients,initialConditions = self._setupEquationParameters(request)
            equation = smp.Eq(
                coefficients[3]*f(variable).diff(variable,3)
                + coefficients[2]*f(variable).diff(variable,2) 
                + coefficients[1]*f(variable).diff(variable) 
                + coefficients[0]*f(variable) 
                + constant, 
                rightHandSide)
            solution = smp.dsolve(equation,ics=initialConditions).simplify()
            returnedEquation = smp.Eq(coefficients[3]*smp.Symbol("y'''") 
                + coefficients[2]*smp.Symbol("y''") 
                + coefficients[1]*smp.Symbol("y'") 
                + coefficients[0]*smp.Symbol("y") 
                + constant, 
                rightHandSide)
            latexifiedEquation,latexifiedSolution = self.latexifyResult(returnedEquation,solution)
            return DifferentialEquationResponse(solution=latexifiedSolution.replace("f{\\left(x \\right)}","y"),equation=latexifiedEquation)
        except Exception as e :
            traceback.print_exc()
            raise e

        
