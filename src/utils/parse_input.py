from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application)


class InputParser :

    @staticmethod
    def parse_expression(origin: str) -> str:
        t = list(origin)
        for i in range(len(t)):
            if t[i] == "^":
                t[i] = "**"
        origin = "".join(t)
        return parse_expr((origin),
                        transformations=(standard_transformations +
                                        (implicit_multiplication_application,)))
    
    @staticmethod
    def parse_equations(origin: str) -> str:
        result = list(origin)
        for i in range(len(result) - 1):
            if result[i].isdigit() and result[i + 1].isalpha():
                result.insert(i + 1, "*")
        return "".join(result)
    



