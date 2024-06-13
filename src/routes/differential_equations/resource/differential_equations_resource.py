from fastapi import APIRouter,HTTPException
from ..domain.models.differential_equation_request import DifferentialEquationRequest
from ..domain.models.differential_equation_response import DifferentialEquationResponse
from ..service.differential_equations_service import DifferentialEquationsService

CONTEXT_PATH = "differential-equations"

differentialEquationsRouter = APIRouter(
    prefix=f"api/v1/{CONTEXT_PATH}",
    tags=["differential-equations"]
)

@differentialEquationsRouter.post("/first", response_model=DifferentialEquationResponse, status_code=200)
async def first_order_differential_equation(request : DifferentialEquationRequest) -> DifferentialEquationResponse :
    try :
        response = DifferentialEquationsService().firstOrderDifferentialEquation(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
@differentialEquationsRouter.post("/second", response_model=DifferentialEquationResponse, status_code=200)
async def second_order_differential_equation(request : DifferentialEquationRequest) -> DifferentialEquationResponse :
    try :
        response = DifferentialEquationsService().secondOrderDifferentialEquation(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
@differentialEquationsRouter.post("/third", response_model=DifferentialEquationResponse, status_code=200)
async def third_order_differential_equation(request : DifferentialEquationRequest) -> DifferentialEquationResponse :
    try :
        response = DifferentialEquationsService().thirdOrderDifferentialEquation(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))