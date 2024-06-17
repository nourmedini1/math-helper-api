import traceback
import sympy as smp
from typing import Union
from routes.product.domain.models.product_request import ProductRequest
from routes.product.domain.models.product_response import ProductResponse
from utils.parse_input import InputParser

class ProductServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ProductServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class ProductService(metaclass= ProductServiceMeta) :

    def _setupLimits(self,lowerLimit : Union[str,int,float], upperLimit : Union[str,int,float]) :
        if lowerLimit == "-oo" : 
            lowerLimit = -smp.oo
        if upperLimit == "oo" :
            upperLimit = smp.oo
        return lowerLimit,upperLimit

    def _setupParameters(self,request : ProductRequest) -> tuple[str] :
        variable = smp.Symbol(request.variable)
        expression = smp.sympify(InputParser.parse_expression(request.expression))
        lowerLimit,upperLimit = self._setupLimits(request.lowerLimit,request.upperLimit)
        return expression,variable,lowerLimit,upperLimit
    
    def symbolicProduct(self, request : ProductRequest) -> ProductResponse :  
        try :      
            expression,variable,lowerLimit,upperLimit = self._setupParameters(request)
            product = smp.Product(expression,(variable,lowerLimit,upperLimit))  
            if product.is_convergent() :
                convergent = True
                try :
                    result = smp.simplify(smp.Product(expression,(variable,lowerLimit,upperLimit)))
                except Exception:
                    result = "no symbolic form found"
            else :
                convergent = False
                result = ""
            return ProductResponse(
                convergent= convergent,
                product = smp.latex(product),
                result = smp.latex(result)
                )
        except Exception as e:
            traceback.print_exc()
            raise e

        
    def numericProduct(self,request : ProductRequest) -> ProductResponse :
        expression,variable,lowerLimit,upperLimit = self._setupParameters(request)
        product = smp.Product(expression,(variable,lowerLimit,upperLimit))
        if product.is_convergent() :
            convergent = True
            try :
                result = smp.N(smp.Product(expression,(variable,lowerLimit,upperLimit)))
            except Exception:
                result = "no numeric form found"
        else :
            convergent = False
            result = ""
        return ProductResponse(
            convergent= convergent,
            product = smp.latex(product),
            result = smp.latex(result)
            )

        