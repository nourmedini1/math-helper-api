from routes.complex.domain.models.complex_operation_request import ComplexOperationRequest
from routes.complex.domain.models.complex_operation_response import ComplexOperationResponse
from routes.complex.domain.models.polar_form_request import PolarFormRequest
from routes.complex.domain.models.polar_form_response import PolarFormResponse
from routes.complex.domain.utils.complex_utils import ComplexUtils
import sympy as smp



class ComplexServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ComplexServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ComplexService(metaclass= ComplexServiceMeta) :

    def convertToPlarForm(self,request : PolarFormRequest) -> PolarFormResponse :
        latexifiedComplexNumber = ComplexUtils.latexifyComplexNumber(real= request.real, imaginary= request.imaginary)
        polarForm = ComplexUtils.createPolarForm(real= request.real , imaginary= request.imaginary)
        return PolarFormResponse(algebraicForm=latexifiedComplexNumber, polarForm=polarForm)

    def _parseComplexInput(self,request : ComplexOperationRequest) -> tuple[str] :
        z1 = ComplexUtils.latexifyComplexNumber(real= request.real1,imaginary=request.imaginary1)
        z2 = ComplexUtils.latexifyComplexNumber(real= request.real2,imaginary=request.imaginary2)
        polarZ1 = ComplexUtils.createPolarForm(real=request.real1, imaginary=request.imaginary1)
        polarZ2 = ComplexUtils.createPolarForm(real=request.real2, imaginary=request.imaginary2)
        return z1,z2,polarZ1,polarZ2

    def _parseComplexOutput(self,real : str , imaginary : str) -> tuple[str] :
        resultAlgebraicForm = ComplexUtils.latexifyComplexNumber(real=real, imaginary=imaginary)
        resultPolarForm = ComplexUtils.createPolarForm(real=real,imaginary=imaginary)
        return resultAlgebraicForm,resultPolarForm

    def addComplexNumbers(self, request: ComplexOperationRequest) -> ComplexOperationResponse:
        try:
            # Parse input strings to SymPy expressions
            real1 = smp.sympify(request.real1)
            real2 = smp.sympify(request.real2)
            imaginary1 = smp.sympify(request.imaginary1)
            imaginary2 = smp.sympify(request.imaginary2)

            # Use parsed values for all further processing
            z1, z2, polarZ1, polarZ2 = self._parseComplexInput(request)
            resultReal = smp.simplify(real1 + real2)
            resultImaginary = smp.simplify(imaginary1 + imaginary2)
            resultAlgebraicForm, resultPolarForm = self._parseComplexOutput(resultReal, resultImaginary)
            return ComplexOperationResponse(
                z1=z1, z2=z2, polarZ1=polarZ1, polarZ2=polarZ2,
                algebraicResult=resultAlgebraicForm, polarResult=resultPolarForm
            )
        except Exception as e:
            raise e

    def substractComplexNumbers(self, request: ComplexOperationRequest) -> ComplexOperationResponse:
        try:
            real1 = smp.sympify(request.real1)
            real2 = smp.sympify(request.real2)
            imaginary1 = smp.sympify(request.imaginary1)
            imaginary2 = smp.sympify(request.imaginary2)

            z1, z2, polarZ1, polarZ2 = self._parseComplexInput(request)
            resultReal = smp.simplify(real1 - real2)
            resultImaginary = smp.simplify(imaginary1 - imaginary2)
            resultAlgebraicForm, resultPolarForm = self._parseComplexOutput(resultReal, resultImaginary)
            return ComplexOperationResponse(
                z1=z1, z2=z2, polarZ1=polarZ1, polarZ2=polarZ2,
                algebraicResult=resultAlgebraicForm, polarResult=resultPolarForm
            )
        except Exception as e:
            raise e

    def multiplyComplexNumbers(self, request: ComplexOperationRequest) -> ComplexOperationResponse:
        try:
            real1 = smp.sympify(request.real1)
            real2 = smp.sympify(request.real2)
            imaginary1 = smp.sympify(request.imaginary1)
            imaginary2 = smp.sympify(request.imaginary2)

            z1, z2, polarZ1, polarZ2 = self._parseComplexInput(request)
            resultReal = smp.simplify(real1 * real2 - imaginary1 * imaginary2)
            resultImaginary = smp.simplify(real1 * imaginary2 + real2 * imaginary1)
            resultAlgebraicForm, resultPolarForm = self._parseComplexOutput(resultReal, resultImaginary)
            return ComplexOperationResponse(
                z1=z1, z2=z2, polarZ1=polarZ1, polarZ2=polarZ2,
                algebraicResult=resultAlgebraicForm, polarResult=resultPolarForm
            )
        except Exception as e:
            raise e
