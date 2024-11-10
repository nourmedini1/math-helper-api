import sympy as smp

class ComplexUtils:

    @staticmethod
    def latexifyComplexNumber(real: str, imaginary: str) -> str:
        real_expr = smp.sympify(real)
        imaginary_expr = smp.sympify(imaginary)
        return smp.latex(real_expr) + ' + ' + smp.latex(imaginary_expr) + 'i'
        
    @staticmethod
    def createPolarForm(real: str, imaginary: str) -> str:
        real_expr = smp.sympify(real)
        imaginary_expr = smp.sympify(imaginary)
        z = real_expr + imaginary_expr * smp.I 
        argument = smp.ratsimp(smp.arg(z))
        modulus = smp.ratsimp(smp.Abs(z))
        return smp.latex(modulus * smp.exp(smp.I * argument))
    
    @staticmethod
    def createAlgebraicForm(real: str, imaginary: str) -> str:
        real_expr = smp.sympify(real)
        imaginary_expr = smp.sympify(imaginary)
        return smp.latex(real_expr + imaginary_expr * smp.I)