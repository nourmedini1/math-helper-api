import sympy as smp
from typing import Union

class ComplexUtils :

    @staticmethod
    def latexifyComplexNumber(real : Union[float,int],imaginary : Union[float,int]) -> str :
        if imaginary < 0 :
            imaginary = -1*imaginary
            return smp.latex(real - smp.I*imaginary)
        else :
            return smp.latex(real + smp.I*imaginary)
        
    @staticmethod
    def createPolarForm(real : Union[float,int] , imaginary : Union[float,int]) -> str :
        z = real + imaginary * smp.I 
        argument = smp.ratsimp(smp.arg(z))
        modulus = smp.ratsimp(smp.Abs(z))
        return smp.latex(modulus * smp.exp(smp.I * argument))
    
    @staticmethod
    def createAlgebraicForm(real : Union[float,int],imaginary : Union[float,int]) -> str:
        return real + imaginary * smp.I






    
