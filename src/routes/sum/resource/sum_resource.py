from fastapi import APIRouter,HTTPException
from src.routes.sum.service.sum_service import SumService
from src.routes.sum.domain.models.sum_request import SumRequest
from src.routes.sum.domain.models.sum_response import SumResponse


CONTEXT_PATH = "sum"

sumRouter = APIRouter(
    prefix=f"/api/v1/{CONTEXT_PATH}",
    tags=[CONTEXT_PATH]
)


@sumRouter.post("/symbolic", response_model=SumResponse, status_code=200)
async def symbolic_sum(request : SumRequest) -> SumResponse :
    try :
        response = SumService().symbolicSum(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    

@sumRouter.post("/numeric", response_model=SumResponse, status_code=200)
async def numeric_sum(request : SumRequest) -> SumResponse :
    try :
        response = SumService().numericSum(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
    
