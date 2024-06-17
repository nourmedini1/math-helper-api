from fastapi import HTTPException,APIRouter
from routes.linear_systems.service.linear_systems_service import LinearSystemsService
from routes.linear_systems.domain.models.linear_system_request import LinearSystemRequest
from routes.linear_systems.domain.models.linear_system_response import LinearSystemResponse

CONTEXT_PATH = "linear-systems"

linearSystemsRouter = APIRouter(
    prefix=f"/api/v1/{CONTEXT_PATH}",
    tags=["Linear Systems"]
)


@linearSystemsRouter.post("/solve", response_model=LinearSystemResponse, status_code=200)
async def linear_system(request : LinearSystemRequest) -> LinearSystemResponse :
    try :
        response = LinearSystemsService().linearSystem(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
    



