from fastapi import APIRouter, HTTPException
from ..domain.models.complex_operation_request import ComplexOperationRequest
from ..domain.models.complex_operation_response import ComplexOperationResponse
from ..domain.models.polar_form_request import PolarFormRequest
from ..domain.models.polar_form_response import PolarFormResponse
from ..service.complex_service import ComplexService



CONTEXT_PATH = "complex"


complexRouter = APIRouter(
    prefix=f"api/v1/{CONTEXT_PATH}",
    tags=["complex-analysis"]
)

async def complex_operation(request : ComplexOperationRequest) -> ComplexOperationResponse :
    try :
        response = ComplexService.applyOperationOnComplexNumbers(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))


@complexRouter.post("/polar-form", response_model=PolarFormResponse, status_code=200)
async def polar_form(request : PolarFormRequest ):
    try :
        response = ComplexService.convertToPlarForm(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))

@complexRouter.post("/add", response_model=ComplexOperationResponse, status_code= 200)
async def complex_addition(request : ComplexOperationRequest) :
    return await complex_operation(request= request)

@complexRouter.post("/subtract", response_model=ComplexOperationResponse, status_code= 200)
async def complex_subtraction(request : ComplexOperationRequest) :
    return await complex_operation(request= request)

@complexRouter.post("/multiply", response_model=ComplexOperationResponse, status_code= 200)
async def complex_multiplication(request : ComplexOperationRequest) :
    return await complex_operation(request= request)

        