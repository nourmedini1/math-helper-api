from fastapi import APIRouter,HTTPException
from routes.integrals.service.integrals_service import IntegralsService
from routes.integrals.domain.models.integral_request import IntegralRequest
from routes.integrals.domain.models.integral_response import IntegralResponse

CONTEXT_PATH = "integrals"

integralsRouter = APIRouter(
    prefix=f"/api/v1/{CONTEXT_PATH}",
    tags=["Integrals"]
)


@integralsRouter.post("/single", response_model=IntegralResponse, status_code=200)
async def single_integral(request : IntegralRequest) -> IntegralResponse :
    try :
        response = IntegralsService().singleIntegral(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
@integralsRouter.post("/double", response_model=IntegralResponse, status_code=200)
async def double_integral(request : IntegralRequest) -> IntegralResponse :
    try :
        response = IntegralsService().doubleIntegral(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))

@integralsRouter.post("/triple", response_model=IntegralResponse, status_code=200)
async def triple_integral(request : IntegralRequest) -> IntegralResponse :
    try :
        response = IntegralsService().tripleIntegral(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))

@integralsRouter.post("/definite/single", response_model=IntegralResponse, status_code=200)
async def definite_single_integral(request : IntegralRequest) -> IntegralResponse :
    try :
        response = IntegralsService().definiteSingleIntegral(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    

@integralsRouter.post("/definite/double", response_model=IntegralResponse, status_code=200)
async def definite_double_integral(request : IntegralRequest) -> IntegralResponse :
    try :
        response = IntegralsService().definiteDoubleIntegral(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    

@integralsRouter.post("/definite/triple", response_model=IntegralResponse, status_code=200)
async def definite_triple_integral(request : IntegralRequest) -> IntegralResponse :
    try :
        response = IntegralsService().definiteTripleIntegral(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    