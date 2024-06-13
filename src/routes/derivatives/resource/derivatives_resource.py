from fastapi import APIRouter, HTTPException
from routes.derivatives.domain.models.derivative_request import DerivativeRequest
from routes.derivatives.domain.models.derivative_response import DerivativeResponse
from routes.derivatives.service.derivatives_service import DerivativesService


CONTEXT_PATH = "derivatives"

derivativesRouter = APIRouter(
    prefix=f"/api/v1/{CONTEXT_PATH}",
    tags=["derivatives"]
) 

@derivativesRouter.post("/symbolic", response_model=DerivativeResponse, status_code=200)
async def symbolic_derivative(request : DerivativeRequest) -> DerivativeResponse :
    try :
        response = DerivativesService().symbolicDerivative(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
@derivativesRouter.post("/numeric", response_model=DerivativeResponse, status_code=200)
async def numeric_derivative(request : DerivativeRequest) -> DerivativeResponse :
    try :
        response = DerivativesService().numericDerivative(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
