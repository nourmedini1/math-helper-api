from fastapi import APIRouter,HTTPException
from routes.limits.service.limits_service import LimitsService
from routes.limits.domain.models.limit_request import LimitRequest
from routes.limits.domain.models.limit_response import LimitResponse


CONTEXT_PATH = "limits"
limitsRouter = APIRouter(prefix=f"/api/v1/{CONTEXT_PATH}", tags=[CONTEXT_PATH])

@limitsRouter.post("/single", response_model=LimitResponse, status_code=200)
async def single_limit(request : LimitRequest) -> LimitResponse :
    try :
        response = LimitsService().singleLimit(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
@limitsRouter.post("/double", response_model=LimitResponse, status_code=200)
async def double_limit(request : LimitRequest) -> LimitResponse :
    try :
        response = LimitsService().doubleLimit(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
@limitsRouter.post("/triple", response_model=LimitResponse, status_code=200)
async def triple_limit(request : LimitRequest) -> LimitResponse :
    try :
        response = LimitsService().tripleLimit(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
