import sympy as smp


class ComplexUtils :

    @staticmethod
    def latexify_complex_number(real,imaginary) :
        if imaginary < 0 :
            imaginary = -1*imaginary
            return smp.latex(real - smp.I*imaginary)
        else :
            return smp.latex(real + smp.I*imaginary)
        
    @staticmethod
    def create_polar_form(complex_number) :
        argument = smp.arg(complex_number)
        modulus = smp.Abs(complex_number)
        return smp.latex(modulus * smp.exp(smp.I * argument))
    
    @staticmethod
    def create_complex_form(real,imaginary) :
        return real + imaginary * smp.I






    
