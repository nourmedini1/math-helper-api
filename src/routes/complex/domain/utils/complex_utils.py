import sympy as smp


class ComplexUtils :

    @staticmethod
    def latexifyComplexNumber(real : float,imaginary : float) -> str :
        if imaginary < 0 :
            imaginary = -1*imaginary
            return smp.latex(real - smp.I*imaginary)
        else :
            return smp.latex(real + smp.I*imaginary)
        
    @staticmethod
    def createPolarForm(complexNumber : str) -> str :
        argument = smp.arg(complexNumber)
        modulus = smp.Abs(complexNumber)
        return smp.latex(modulus * smp.exp(smp.I * argument))
    
    @staticmethod
    def createAlgebraicForm(real : float,imaginary : float) -> str:
        return real + imaginary * smp.I






    
