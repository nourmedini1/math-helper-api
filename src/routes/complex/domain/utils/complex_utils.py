import sympy as smp

class ComplexUtils :

    @staticmethod
    def latexifyComplexNumber(real : str,imaginary : str) -> str :
        return smp.latex(real + smp.I*imaginary)
        
    @staticmethod
    def createPolarForm(real : str , imaginary : str) -> str :
        z = real + imaginary * smp.I 
        argument = smp.ratsimp(smp.arg(z))
        modulus = smp.ratsimp(smp.Abs(z))
        return smp.latex(modulus * smp.exp(smp.I * argument))
    
    @staticmethod
    def createAlgebraicForm(real : str,imaginary : str) -> str:
        return real + imaginary * smp.I






    
