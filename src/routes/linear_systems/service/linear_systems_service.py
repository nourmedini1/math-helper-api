from routes.linear_systems.domain.models.linear_system_request import LinearSystemRequest
from routes.linear_systems.domain.models.linear_system_response import LinearSystemResponse
from utils.parse_input import InputParser
import sympy as smp
from typing import List, Union


class LinearSystemsServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(LinearSystemsServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class LinearSystemsService(metaclass= LinearSystemsServiceMeta) :

    LATEX_BEGIN = "\\begin{cases} "
    LATEX_END = "\\end{cases}"
    LATEX_SEPERATOR = "\\\\ "

    def _setupEquations(self,equations : List[str] ,rightHandSide : List[str]) -> List :
        parsedEquations = list(map(InputParser.parse_equations,equations))
        sympifiedEquations = [smp.Eq(smp.parse_expr(parsedEquations[i]),rightHandSide[i]) for i in range(len(equations))]
        return sympifiedEquations
    
    def _setupRightHandSide(self,rhs : List[Union[str,int,float]]) -> List[float] :
        return list(map(float,rhs))
    
    def _setupVariables(self,variables : List[str]) -> List[smp.Symbol] :
        return list(map(smp.Symbol,variables))
    
    def _latexifyEquations(equations : List) -> List[str] : 
        return list(map(smp.latex,equations))

    def _latexifyLinearSystem(latexifiedEquations : list[str]) :
        linearSystem = ""
        for i in range(len(latexifiedEquations)-1) :
            linearSystem += latexifiedEquations[i] + LinearSystemsService.LATEX_SEPERATOR
        linearSystem += latexifiedEquations[-1]
        return LinearSystemsService.LATEX_BEGIN + linearSystem + LinearSystemsService.LATEX_END
    
    def _solveLinearSystem(self,equations : List[smp.Eq],variables : List[smp.Symbol]) -> List :
        return list(smp.linsolve(equations,tuple(variables)))
    
    def _latexifyResults(self,results : List,variables : List) -> str :
        resultList = [smp.latex(variables[i]) + " = " + smp.latex(results[0][i]) for i in range(len(results[0]))]
        latexResults = ""
        for result in resultList :
            latexResults += smp.latex(result) + LinearSystemsService.LATEX_SEPERATOR
        return latexResults
    
    def linearSystem(self, request : LinearSystemRequest) -> LinearSystemResponse:
        rightHandSide = self._setupRightHandSide(request.righHandSide)
        equations = self._setupEquations(request.equations,rightHandSide)
        variables = self._setupVariables(request.variables)
        results = self._solveLinearSystem(equations,variables)
        latexifiedEquations = self._latexifyEquations(equations)
        latexifiedLinearSystem = self._latexifyLinearSystem(latexifiedEquations)
        latexifiedResults = self._latexifyResults(results,variables)
        return LinearSystemResponse(
            linearSystem = latexifiedLinearSystem,
            result = latexifiedResults
        )
  

    


