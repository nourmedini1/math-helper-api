from ..domain.models.complex_operation_request import ComplexOperationRequest
from ..domain.models.complex_operation_response import ComplexOperationResponse
from ..domain.models.polar_form_request import PolarFormRequest
from ..domain.models.polar_form_response import PolarFormResponse
from ..domain.utils.complex_utils import ComplexUtils


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
    
    def applyOperationOnComplexNumbers(self,request : ComplexOperationRequest) -> ComplexOperationResponse :
        algebraicForm : str = None
        polarForm : str = None
        try :
            if request.operation == "ADDITION" :
                algebraicForm, polarForm = self._addComplexNumbers(
                    real1=request.real1, real2=request.real2, imaginary1=request.imaginary1, imaginary2=request.imaginary2)
            elif request.operation == "SUBTRACTION" :
                algebraicForm, polarForm = self._subtractComplexNumbers(
                    real1=request.real1, real2=request.real2, imaginary1=request.imaginary1, imaginary2=request.imaginary2)
            elif request.operation == "MULTIPLICATION" :
                algebraicForm, polarForm = self._multiplyComplexNumbers(
                    real1=request.real1, real2=request.real2, imaginary1=request.imaginary1, imaginary2=request.imaginary2)
            return ComplexOperationResponse(
                z1= ComplexUtils.createAlgebraicForm(real=request.real1, imaginary=request.imaginary1),
                z2= ComplexUtils.createAlgebraicForm(real=request.real2, imaginary=request.imaginary2),
                polarZ1= ComplexUtils.createPolarForm(ComplexUtils.createAlgebraicForm(real=request.real1, imaginary=request.imaginary1)),
                polarZ2= ComplexUtils.createPolarForm(ComplexUtils.createAlgebraicForm(real=request.real2, imaginary=request.imaginary2)),
                algebraicResult=algebraicForm,
                polarResult=polarForm
                )
        except Exception as e :
            raise e 

    def _addComplexNumbers(real1 : float , real2 : float, imaginary1 : float, imaginary2 : float) -> tuple[str] :
        resultAlgebraicForm = ComplexUtils.createAlgebraicForm(real=real1+real2, imaginary=imaginary1+imaginary2)
        resultPolarForm = ComplexUtils.createPolarForm(resultAlgebraicForm)
        return resultAlgebraicForm, resultPolarForm
    
    def _subtractComplexNumbers(real1 : float , real2 : float, imaginary1 : float, imaginary2 : float) -> tuple[str] :
        resultAlgebraicForm = ComplexUtils.createAlgebraicForm(real=real1-real2, imaginary=imaginary1-imaginary2)
        resultPolarForm = ComplexUtils.createPolarForm(resultAlgebraicForm)
        return resultAlgebraicForm, resultPolarForm
    
    def _multiplyComplexNumbers(real1 : float , real2 : float, imaginary1 : float, imaginary2 : float) -> tuple[str] :
        resultAlgebraicForm = ComplexUtils.createAlgebraicForm(
            real=real1*real2 - imaginary1*imaginary2,
            imaginary=real1*imaginary2 + real2*imaginary1)
        resultPolarForm = ComplexUtils.createPolarForm(resultAlgebraicForm)
        return resultAlgebraicForm, resultPolarForm
    