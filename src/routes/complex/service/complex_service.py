from routes.complex.domain.models.complex_operation_request import ComplexOperationRequest
from routes.complex.domain.models.complex_operation_response import ComplexOperationResponse
from routes.complex.domain.models.polar_form_request import PolarFormRequest
from routes.complex.domain.models.polar_form_response import PolarFormResponse
from routes.complex.domain.utils.complex_utils import ComplexUtils



class ComplexServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ComplexServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ComplexService(metaclass= ComplexServiceMeta) :

    def convertToPlarForm(self,request : PolarFormRequest) -> PolarFormResponse :
        complexNumber = ComplexUtils.createAlgebraicForm(real= request.real, imaginary= request.imaginary)
        latexifiedComplexNumber = ComplexUtils.latexifyComplexNumber(real= request.real, imaginary= request.imaginary)
        polarForm = ComplexUtils.createPolarForm(complexNumber)
        return PolarFormResponse(algebraicForm=latexifiedComplexNumber, polarForm=polarForm)
    
    def _parseComplexInput(self,request : ComplexOperationRequest) -> tuple[str] :
        z1 = ComplexUtils.latexifyComplexNumber(real= request.real1,imaginary=request.imaginary1)
        z2 = ComplexUtils.latexifyComplexNumber(real= request.real2,imaginary=request.imaginary2)
        polarZ1 = ComplexUtils.createPolarForm(ComplexUtils.createAlgebraicForm(real=request.real1, imaginary=request.imaginary1))
        polarZ2 = ComplexUtils.createPolarForm(ComplexUtils.createAlgebraicForm(real=request.real2, imaginary=request.imaginary2))
        return z1,z2,polarZ1,polarZ2
    
    def _parseComplexOutput(self,real : float , imaginary : float) -> tuple[str] : 
        resultAlgebraicForm = ComplexUtils.latexifyComplexNumber(real=real, imaginary=imaginary)
        resultPolarForm = ComplexUtils.createPolarForm(ComplexUtils.createAlgebraicForm(real=real,imaginary=imaginary))
        return resultAlgebraicForm,resultPolarForm

    def addComplexNumbers(self,request : ComplexOperationRequest) -> ComplexOperationResponse:
        try :
            z1,z2,polarZ1,polarZ2 = self._parseComplexInput(request)
            resultReal = request.real1+request.real2
            resultImaginary = request.imaginary1+request.imaginary2
            resultAlgebraicForm,resultPolarForm = self._parseComplexOutput(resultReal,resultImaginary)
            return ComplexOperationResponse(z1=z1, z2=z2, polarZ1=polarZ1, polarZ2=polarZ2, algebraicResult=resultAlgebraicForm, polarResult=resultPolarForm)
        except Exception as e:
            raise e
        
    def substractComplexNumbers(self,request : ComplexOperationRequest) -> ComplexOperationResponse :
        try :
            z1,z2,polarZ1,polarZ2 = self._parseComplexInput(request)
            resultReal = request.real1-request.real2
            resultImaginary = request.imaginary1-request.imaginary2
            resultAlgebraicForm,resultPolarForm = self._parseComplexOutput(resultReal,resultImaginary)
            return ComplexOperationResponse(z1=z1, z2=z2, polarZ1=polarZ1, polarZ2=polarZ2, algebraicResult=resultAlgebraicForm, polarResult=resultPolarForm)
        except Exception as e:
            raise e
        
    def multiplyComplexNumbers(self,request : ComplexOperationRequest) -> ComplexOperationResponse :
        try :
            z1,z2,polarZ1,polarZ2 = self._parseComplexInput(request)
            resultReal = request.real1*request.real2 - request.imaginary1*request.imaginary2
            resultImaginary = request.real1*request.imaginary2 + request.real2*request.imaginary1
            resultAlgebraicForm,resultPolarForm = self._parseComplexOutput(resultReal,resultImaginary)
            return ComplexOperationResponse(z1=z1, z2=z2, polarZ1=polarZ1, polarZ2=polarZ2, algebraicResult=resultAlgebraicForm, polarResult=resultPolarForm)
        except Exception as e:
            raise e
        
            
       
      
    
   